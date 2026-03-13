import json
import os

from kafka import KafkaProducer


KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "127.0.0.1:9092")

producer = None


def get_producer():
    global producer
    if producer is None:
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )
    return producer


def send_event(topic, data):
    try:
        p = get_producer()
        p.send(topic, data)
        p.flush()
    except Exception as exc:
        # Keep core API operations available when Kafka is offline.
        print(f"[kafka-producer] skipping event publish: {exc}", flush=True)