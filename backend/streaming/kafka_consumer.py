import json
import os

from kafka import KafkaConsumer


KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "127.0.0.1:9092")


def start_consumer(topic):

    consumer = KafkaConsumer(

        topic,

        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,

        value_deserializer=lambda x: json.loads(x.decode("utf-8"))

    )

    for message in consumer:

        yield message.value