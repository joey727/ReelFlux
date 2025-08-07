import pika
import os


from main import sendEmail


def main():
    """function for sending notifications"""

    # configure rabbitmq connection
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    def callback(channel, method, body):
        err = sendEmail.notification(body)
        if err:
            channel.basic_nack(delivery_tag=method.delivery_tag)
        else:
            channel.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(queue=os.getenv('MP3_QUEUE'),
                          on_message_callback=callback)

    print('Awaiting messages from queue, CTRL C to exit')
    channel.start_consuming()


if __name__ == "__main__":
    main()
