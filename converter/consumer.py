import pika
import os
from pymongo import MongoClient
import gridfs
from convert import to_mp3
from dotenv import load_dotenv

load_dotenv()


def main():
    client = MongoClient("host.minikube.internal", 27017)
    videos_db = client.videos_db
    mp3_db = client.mp3s

    fs_videosDb = gridfs.GridFS(videos_db)
    fs_mp3Db = gridfs.GridFS(mp3_db)

    # configure rabbitmq connection
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    def callback(channel, method, properties, body):
        err = to_mp3.start(body, fs_videosDb, fs_mp3Db, channel)
        if err:
            channel.basic_nack(delivery_tag=method.delivery_tag)
        else:
            channel.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue=os.getenv('VIDEO_QUEUE'),
                          on_message_callback=callback)

    print('Awaiting messages from queue, CTRL C to exit')
    channel.start_consuming()


if __name__ == "__main__":
    main()
