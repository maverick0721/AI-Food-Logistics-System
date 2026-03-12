def assign_driver(order_id):

    driver_id = order_id % 10

    return {

        "order_id": order_id,
        "driver_id": driver_id

    }