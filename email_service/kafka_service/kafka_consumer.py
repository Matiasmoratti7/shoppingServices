from kafka import KafkaConsumer
from exceptions import exceptions
import json
from config import config

kafka_instance = None


def get_kafka_producer():
    global kafka_instance
    if kafka_instance is None:
        try:
            kafka_instance = KafkaConsumer(config.configs.kafka_topic,
                                           bootstrap_servers=[config.configs.kafka_bootstrap_server],
                                           auto_offset_reset='earliest',
                                           consumer_timeout_ms=1000)
        except Exception:
            raise exceptions.CustomError("Error when trying to connect to Kafka Server")
    return kafka_instance


def consume_messages():
    messages = []
    for msg in get_kafka_producer():
        record = json.loads(msg.value)
        messages.append(record)
    return messages

