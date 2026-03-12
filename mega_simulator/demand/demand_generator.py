import numpy as np


class DemandGenerator:

    def generate_orders(self, hour):

        base = 200

        if 12 <= hour <= 14:
            base *= 3

        if 19 <= hour <= 21:
            base *= 4

        return np.random.poisson(base)