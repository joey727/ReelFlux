import smtplib
import json
import os

from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()


def notification(message):
    """nofication logic"""
    try:
        message = json.loads(message)
        mp3file_id = message['mp3file_id']
        sender_email = os.getenv('EMAIL_ADDRESS', 'joey@xxx.com')
        sender_password = os.getenv('EMAIL_PASSWORD', 'Password11234')
        reciever = message['user_id']

        MESSAGE = EmailMessage()
        MESSAGE.set_content(f"File ID: {mp3file_id} convertion successfull. \
                            Go ahead and download via '/download' in url")
        MESSAGE["Subject"] = "DOWNLOAD FILE READY"
        MESSAGE["From"] = sender_email
        MESSAGE["TO"] = reciever

        # connect to google SMTP
        session = smtplib.SMTP("smtp.gmail.com", 587)
        session.starttls()
        session.login(sender_email, sender_password)
        session.send_message(MESSAGE, sender_email, reciever)

        # finally close session
        session.quit()
    except Exception as e:
        print(e)
        return str(e)
