from flask import Flask, request
import os
import datetime
import jwt
import pymysql


app = Flask(__name__)

# configuration
db_config = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'rootAdmin'),
    'database': os.getenv('DB_NAME', 'auth_db'),
    'port': int(os.getenv('DB_PORT', 3306))
}


def connect_db():
    try:
        connection = pymysql.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database'],
            port=db_config['port']
        )
        return connection
    except pymysql.MySQLError as e:
        print(f"Error connecting to database: {e}")
        return None
    finally:
        if connection:
            connection.close()

# basic login function


@app.route('/login', methods=['POST'])
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return {'message': 'Could not verify'}, 401
