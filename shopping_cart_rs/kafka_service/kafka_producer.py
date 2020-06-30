from kafka import KafkaProducer
from exceptions import exceptions
import json
from config import config

kafka_instance = None


def get_kafka_producer():
    global kafka_instance
    if kafka_instance is None:
        try:
            kafka_instance = KafkaProducer(bootstrap_servers=[config.configs.kafka_bootstrap_server],
                                           value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        except Exception:
            raise exceptions.CustomError("Error when trying to connect to Kafka Server", 500)
    return kafka_instance


def send_message(json_message):
    producer = get_kafka_producer()
    try:
        producer.send(config.configs.kafka_topic, json_message)
        producer.flush()
    except Exception:
        raise exceptions.CustomError("Error when trying to connect to send message to Kafka Server", 500)