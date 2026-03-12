import os

_model = None


def _get_model():
    global _model
    if _model is None:
        import torch
        from ml_models.recommendation.model import TwoTowerModel

        _model = TwoTowerModel()
        model_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "models",
            "recommendation_model.pt",
        )
        _model.load_state_dict(torch.load(model_path, weights_only=True))
        _model.eval()
    return _model


def predict(user_id, restaurant_id):
    import torch

    model = _get_model()

    user = torch.tensor([user_id])
    restaurant = torch.tensor([restaurant_id])

    with torch.no_grad():
        score = model(user, restaurant)

    return score.item()


if __name__ == "__main__":

    s = predict(10, 5)

    print("Recommendation score:", s)