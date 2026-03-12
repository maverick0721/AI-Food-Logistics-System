from data_pipeline.ingestion.order_generator import OrderGenerator
from utils.dataset import save_parquet


def run():

    generator = OrderGenerator(20000)

    df = generator.generate()

    save_parquet(df, "datasets/raw/orders.parquet")

    print("Dataset saved")


if __name__ == "__main__":
    run()