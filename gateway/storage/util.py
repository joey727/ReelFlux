import pika
import json


def upload_file(fs, file, channel, access):
    try:
        file_id = fs.put(file)
        message = {
            'file_id': str(file_id),
            'mp3file_id': None,  # Assuming no mp3 conversion for simplicity
            'user_id': access['user_id']
        }
        channel.basic_publish(exchange='', routing_key='file.upload', body=json.dumps(message),
                              properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))
        return None
    except Exception as e:
        return str(e)
