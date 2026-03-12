import random


class TrafficModel:

    def get_speed(self, hour):

        if 8 <= hour <= 10:
            return random.uniform(15, 25)

        if 18 <= hour <= 21:
            return random.uniform(10, 20)

        return random.uniform(30, 40)