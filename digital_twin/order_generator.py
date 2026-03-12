import random


class OrderGenerator:

    def generate(self):

        return {

            "pickup": random.randint(0, 500),
            "drop": random.randint(0, 500)

        }