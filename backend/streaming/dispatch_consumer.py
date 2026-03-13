from backend.streaming.kafka_consumer import start_consumer
from backend.streaming.topics import ORDER_CREATED
import time


def run():
    while True:
        try:
            for event in start_consumer(ORDER_CREATED):
                print("New order received:", event, flush=True)
                # Here we will later call RL dispatch
        except Exception as exc:
            print(f"[dispatch-consumer] Kafka unavailable, retrying in 5s: {exc}", flush=True)
            time.sleep(5)


if __name__ == "__main__":

    run()