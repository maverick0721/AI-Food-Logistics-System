from backend.streaming.kafka_producer import send_event
from backend.streaming.topics import ORDER_CREATED

def assign_driver(order_id):

    driver_id = order_id % 10

    # Send event to Kafka
    send_event(

    ORDER_CREATED,

    {

        "order_id": db_order.id,
        "user_id": order.user_id,
        "restaurant_id": order.restaurant_id

    }

)

    return {

        "order_id": order_id,
        "driver_id": driver_id

    }