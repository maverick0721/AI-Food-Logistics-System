import random


class Restaurant:

    def __init__(self, restaurant_id, location):

        self.id = restaurant_id
        self.location = location

    def prep_time(self):

        return random.randint(5, 20)