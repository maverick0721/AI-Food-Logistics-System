import random


class TrafficModel:

    def get_speed(self, hour):

        if 8 <= hour <= 10:
            return random.uniform(10, 20)

        if 17 <= hour <= 20:
            return random.uniform(8, 18)

        return random.uniform(25, 40)