import pandas as pd
import numpy as np


class OrderGenerator:

    def __init__(self, n_orders=10000):

        self.n_orders = n_orders

    def generate(self):

        data = {

            "distance": np.random.uniform(1, 10, self.n_orders),

            "traffic": np.random.randint(1, 5, self.n_orders),

            "prep_time": np.random.uniform(5, 20, self.n_orders),

            "driver_load": np.random.randint(1, 4, self.n_orders),

        }

        df = pd.DataFrame(data)

        df["eta"] = (
            df["distance"] * 4
            + df["traffic"] * 3
            + df["prep_time"]
            + df["driver_load"] * 2
        )

        return df