from utils.dataset import load_parquet, save_parquet
from data_pipeline.processing.cleaning import clean
from data_pipeline.processing.feature_engineering import add_features


def build_dataset():

    df = load_parquet("datasets/raw/orders.parquet")

    df = clean(df)

    df = add_features(df)

    save_parquet(df, "datasets/features/orders_features.parquet")

    print("Feature dataset created")


if __name__ == "__main__":
    build_dataset()