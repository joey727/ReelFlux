from time import timezone
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
    'port': int(os.getenv('DB_PORT', 3306))
}


def connect_db():
    try:
        connection = pymysql.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
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
SECRET_KEY = 'keynotsosecret'
ALGORITHM = 'HS256'


@app.route('/login', methods=['POST'])
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return {'message': 'Could not verify'}, 401
    connection = connect_db()
    if not connection:
        return {'message': 'Database connection failed'}, 500
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM users WHERE email = %s", (auth.username,))
            user = cursor.fetchone()
            if not user or user['password'] != auth.password:
                return {'message': 'Invalid credentials'}, 401

            token = jwt.encode({
                'user_id': user['id'],
                'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
            }, SECRET_KEY, algorithm=ALGORITHM)

            return {'token': token}, 200
    except pymysql.MySQLError as e:
        print(f"Database error: {e}")
        return {'message': 'Database error'}, 500


# validate token function
@app.route('/validate', methods=['POST'])
def validate():
    token = request.headers.get('Authorization')
    if not token:
        return {'message': 'Token is missing'}, 401

    token = token.split(" ")[1]  # Assuming the format is "Bearer <token>"
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {'message': 'Token is valid', 'user_id': decoded['user_id']}, 200
    except jwt.ExpiredSignatureError:
        return {'message': 'Token has expired'}, 401
    except jwt.InvalidTokenError:
        return {'message': 'Invalid token'}, 401


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
