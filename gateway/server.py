from flask import Flask, request
from flask_pymongo import PyMongo
import os
import json
import logging
import gridfs
import pika
from auth_request import access_control, validate
from storage import util


server = Flask(__name__)
server.config['MONGO_URI'] = os.getenv(
    'MONGO_URI', 'mongodb://host.minikube.internal:27017/videos_db')
mongo = PyMongo(server)

# Initialize GridFS for file storage
fs = gridfs.GridFS(mongo.db)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()


@server.route('/login', methods=['POST'])
def login():
    token, status = access_control(request)

    if status[0] != 200:
        return status[1], status[0]
    return token


@server.route('/upload', methods=['POST'])
def upload():
    data, status = validate(request)
    if status[0] != 200:
        return status[1], status[0]

    access = json.loads(data)
    if access['user_id']:
        file = request.files.get('file')
        if not file:
            return 'No file uploaded', 400

        err = util.upload_file(fs, file, channel, access)
        if err:
            return err
        return 'File uploaded successfully', 200
    else:
        return 'Unexpected error occured', 401


@server.route('/download', methods=['GET'])
def download():
    data, status = validate(request)
    if status[0] != 200:
        return status[1], status[0]

    access = json.loads(data)
    if access['user_id']:
        file_id = request.args.get('file_id')
        if not file_id:
            return 'File ID is required', 400

        file_data = util.download_file(fs, file_id)
        if not file_data:
            return 'File not found', 404

        return file_data, 200
    else:
        return 'Not Authorized', 401


if __name__ == '__main__':
    server.run(debug=True, host='0.0.0', port=8080)
# gateway/server.py
# This file is the main entry point for the gateway server, handling authentication and file operations.
