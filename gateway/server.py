from flask import Flask, request, send_file
from flask_pymongo import PyMongo
import os
import json
import logging
import gridfs
import pika
from auth_request import access_control, validate
from storage import util
from bson.objectid import ObjectId


server = Flask(__name__)

mongo_videos = PyMongo(
    server, uri="mongodb://host.minikube.internal:27017/videos_db")
mongo_mp3 = PyMongo(
    server, uri="mongodb://host.minikube.internal:27017/mp3s_db")

# Initialize GridFS for file storage
fs_video = gridfs.GridFS(mongo_videos)
fs_mp3 = gridfs.GridFS(mongo_mp3)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()


@server.route('/login', methods=['POST'])
def login():
    token, status = access_control.access_control(request)

    if not token:
        return {"message": "Authentication failed"}, status
    return {"token": token}, 200


@server.route('/upload', methods=['POST'])
def upload():
    data, status = validate.validate(request)
    if status != 200:
        return "Validation error", status

    access = json.loads(data)
    if access['user_id']:
        file = request.files.get('file')
        if not file:
            return 'No file uploaded', 400

        err = util.upload_file(fs_video, file, channel, access)
        if err:
            return err
        return 'File uploaded successfully', 200
    else:
        return 'Unexpected error occured', 401


@server.route('/download', methods=['GET'])
def download():
    data, status = validate.validate(request)
    if status != 200:
        return "Validation error", status

    access = json.loads(data)
    if access['user_id']:
        file_id = request.args.get('file_id')
        if not file_id:
            return 'File ID is required', 400

        try:
            file = fs_mp3.get(ObjectId(file_id))
            return send_file(file, download_name=f"{file_id}.mp3")

        except Exception as e:
            print(e)
            return "Internal Server Error", 500

    else:
        return 'Not Authorized', 401


if __name__ == '__main__':
    server.run(debug=True, host='0.0.0', port=8080)
# gateway/server.py
# This file is the main entry point for the gateway server, handling authentication and file operations.
