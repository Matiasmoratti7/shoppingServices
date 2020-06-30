import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from exceptions import exceptions
from config import config
from kafka_service import kafka_consumer
import time

STAGE = '/ini/config.ini'


def set_server():
    try:
        server = smtplib.SMTP_SSL()
        server = smtplib.SMTP_SSL(host=config.configs.email_host, port=465)
        server.login(config.configs.sender_email, config.configs.sender_pswd)
    except Exception:
        raise exceptions.CustomError("Error when trying to login to {}".format(config.configs.sender_email))
    return server


def send_email(server, subject, body):
    msg = MIMEMultipart()
    msg['From'] = config.configs.sender_email
    msg['To'] = config.configs.manager_email
    msg['Subject'] = "ShoppingCartAPI notification: " + subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server.send_message(msg)
    except Exception:
        raise exceptions.CustomError("Error when trying to send email")

    del msg


def run(config_file):
    config.set_configs(config_file)
    email_server = set_server()
    print("Email service starting...")
    messages = []
    while True:
        try:
            print("Email service is getting messages from Kafka server")
            messages.extend(kafka_consumer.consume_messages())
            print("Email service will process {} messages".format(len(messages)))
            while messages:
                msg = messages.pop()
                send_email(email_server, msg['subject'], msg['body'])
            print("Email service finished processing new messages")
        except exceptions.CustomError as error:
            print(error.message)
            time.sleep(120)
        else:
            time.sleep(60)


if __name__ == "__main__":
    run(config_file=STAGE)


