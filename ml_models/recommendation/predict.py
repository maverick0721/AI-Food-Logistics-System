import torch

from ml_models.recommendation.model import TwoTowerModel


def predict(user_id, restaurant_id):

    model = TwoTowerModel()

    model.load_state_dict(
        torch.load("models/recommendation_model.pt")
    )

    model.eval()

    user = torch.tensor([user_id])
    restaurant = torch.tensor([restaurant_id])

    score = model(user, restaurant)

    return score.item()


if __name__ == "__main__":

    s = predict(10, 5)

    print("Recommendation score:", s)