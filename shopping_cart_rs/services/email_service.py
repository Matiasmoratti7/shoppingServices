from kafka_service import kafka_producer


def send_email(subject, body):
    kafka_producer.send_message({"subject": subject, "body": body})