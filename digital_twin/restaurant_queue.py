import random


class Restaurant:

    def __init__(self, restaurant_id):

        self.restaurant_id = restaurant_id
        self.queue = []

    def add_order(self, order):

        self.queue.append(order)

    def process(self):

        if self.queue:

            prep_time = random.uniform(5, 15)

            order = self.queue.pop(0)

            return order, prep_time

        return None, 0