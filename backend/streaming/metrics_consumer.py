from backend.streaming.kafka_consumer import start_consumer
from backend.streaming.topics import DELIVERY_COMPLETED


def run():

    for event in start_consumer(DELIVERY_COMPLETED):

        print("Delivery completed:", event)


if __name__ == "__main__":

    run()