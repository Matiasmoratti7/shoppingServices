import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from exceptions import exceptions
from config import config
from kafka_service import kafka_consumer
import time

EMAIL_SERVER = smtplib.SMTP_SSL()


def set_server():
    global EMAIL_SERVER
    EMAIL_SERVER = smtplib.SMTP_SSL(host=config.configs.email_host, port=465)
    EMAIL_SERVER.login(config.configs.sender_email, config.configs.sender_pswd)


def send_email(subject, body):

    msg = MIMEMultipart()
    msg['From'] = config.configs.sender_email
    msg['To'] = config.configs.manager_email
    msg['Subject'] = "ShoppingCartAPI notification: " + subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        EMAIL_SERVER.send_message(msg)
    except Exception:
        raise exceptions.EmailServerError()

    del msg


if __name__ == "__main__":
    messages = []
    while True:
        try:
            messages.extend(kafka_consumer.consume_messages())
            while messages:
                msg = messages.pop()
                send_email(msg['subject'], msg['body'])
        except Exception:
            # Log error and sleep for 2 minutes
            time.sleep(120)
        else:
            time.sleep(60)


