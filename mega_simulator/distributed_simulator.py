import ray
import pandas as pd
import random

ray.init()


@ray.remote
class ZoneSimulator:

    def __init__(self, zone_id):

        self.zone_id = zone_id

    def simulate_orders(self, n):

        orders = []

        for i in range(n):

            orders.append({

                "zone": self.zone_id,
                "distance": random.uniform(1, 10),
                "prep_time": random.uniform(5, 20),
                "traffic": random.randint(1, 5)

            })

        return orders


def main():

    # Create zone simulators
    zones = [ZoneSimulator.remote(i) for i in range(10)]

    # Run simulation in parallel
    results = ray.get([z.simulate_orders.remote(100000) for z in zones])

    # Flatten results
    all_orders = []

    for zone_orders in results:

        all_orders.extend(zone_orders)

    df = pd.DataFrame(all_orders)

    df.to_parquet("datasets/raw/simulator_orders.parquet")

    print("Simulation complete")
    print("Total orders:", len(df))


if __name__ == "__main__":

    main()