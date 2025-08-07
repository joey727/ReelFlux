import tempfile
import moviepy
import pika
import json
import os
from bson.objectid import ObjectId
from moviepy import *
from dotenv import load_dotenv

load_dotenv()


def start(message, fs_videosDb, fs_mp3Db, channel):
    message = json.loads(message)
    tf = tempfile.NamedTemporaryFile()
    # get video contents
    out = fs_videosDb.get(ObjectId(message["file_id"]))
    tf.write(out.read())  # this adds the video contents to an empty file

    audio = moviepy.VideoFileClip(tf.name).audio
    tf.close()

    # write audio to file
    tf_path = tempfile.gettempdir() + f"/{message['file_id']}.mp3"
    audio.write_audiofile(tf_path)

    # save audio file to mongo db
    audio_file = open(tf_path, 'rb')
    data = audio_file.read()
    file_id = fs_mp3Db.put(data)
    audio_file.close()
    os.remove(tf_path)

    # update message and put response back in queue
    message['mp3file_id'] = file_id

    try:
        channel.basic_publish(exchange='', routing_key=os.getenv('MP3_QUEUE'), body=json.dumps(
            message), properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE), )
    except Exception as err:
        fs_mp3Db.delete(file_id)
        return err
