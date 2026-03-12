import pandas as pd
import numpy as np


class DemandDataGenerator:

    def __init__(self, days=60):

        self.days = days

    def generate(self):

        hours = self.days * 24

        demand = []

        for h in range(hours):

            hour_of_day = h % 24

            base = 100

            if 12 <= hour_of_day <= 14:
                base *= 2

            if 19 <= hour_of_day <= 21:
                base *= 3

            noise = np.random.normal(0, 10)

            demand.append(base + noise)

        df = pd.DataFrame({

            "hour": range(hours),
            "demand": demand

        })

        return df