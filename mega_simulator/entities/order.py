class Order:

    def __init__(self, order_id, restaurant, customer):

        self.id = order_id

        self.restaurant = restaurant
        self.customer = customer

        self.driver = None