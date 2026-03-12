from ml_models.demand_forecasting.demand_data_generator import DemandDataGenerator


def main():

    generator = DemandDataGenerator()

    df = generator.generate()

    df.to_parquet("datasets/raw/demand_timeseries.parquet")

    print("Demand dataset created")


if __name__ == "__main__":

    main()