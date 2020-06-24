import time, queue, requests
from config import config

emails_queue = queue.Queue()


def start_service():
    while True:
        call_email_service()
        time.sleep(10)


def call_email_service():
    while not emails_queue.empty():
        email = emails_queue.get()
        try:
            requests.post(config.endpoints.email_send, json={"subject": email['subject'], "body": email['body']})
        except Exception:
            emails_queue.put(email)
            # Dejar un log de que hubo un error con el envio del mail


def send_email(subject, body):
    emails_queue.put({"subject": subject, "body": body})
