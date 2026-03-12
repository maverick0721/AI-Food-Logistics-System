from backend.streaming.kafka_consumer import start_consumer
from backend.streaming.topics import ORDER_CREATED


def run():

    for event in start_consumer(ORDER_CREATED):

        print("New order received:", event, flush=True)

        # Here we will later call RL dispatch


if __name__ == "__main__":

    run()