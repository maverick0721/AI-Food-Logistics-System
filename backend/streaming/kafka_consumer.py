import json

from kafka import KafkaConsumer


def start_consumer(topic):

    consumer = KafkaConsumer(

        topic,

        bootstrap_servers="localhost:9092",

        value_deserializer=lambda x: json.loads(x.decode("utf-8"))

    )

    for message in consumer:

        yield message.value