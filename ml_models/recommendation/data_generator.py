import pandas as pd
import numpy as np


class RecommendationDataGenerator:

    def __init__(self, users=500, restaurants=200, interactions=10000):

        self.users = users
        self.restaurants = restaurants
        self.interactions = interactions

    def generate(self):

        data = {

            "user_id": np.random.randint(0, self.users, self.interactions),
            "restaurant_id": np.random.randint(0, self.restaurants, self.interactions),
            "rating": np.random.randint(1, 6, self.interactions),
        }

        return pd.DataFrame(data)