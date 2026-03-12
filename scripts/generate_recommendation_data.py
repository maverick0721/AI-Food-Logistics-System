from ml_models.recommendation.data_generator import RecommendationDataGenerator


def main():

    generator = RecommendationDataGenerator()

    df = generator.generate()

    df.to_parquet("datasets/raw/recommendation_data.parquet")

    print("Recommendation dataset created")


if __name__ == "__main__":

    main()