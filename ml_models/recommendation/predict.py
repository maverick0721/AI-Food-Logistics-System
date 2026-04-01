import os

_model = None


def _fallback_score(user_id, restaurant_id):
    # Deterministic fallback for local/dev runs when trained weights are unavailable.
    seed = (int(user_id) * 31 + int(restaurant_id) * 17) % 100
    return round(seed / 100.0, 4)


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
        if not os.path.exists(model_path):
            return None
        _model.load_state_dict(torch.load(model_path, weights_only=True))
        _model.eval()
    return _model


def predict(user_id, restaurant_id):
    model = _get_model()

    if model is None:
        return _fallback_score(user_id, restaurant_id)

    import torch

    user = torch.tensor([user_id])
    restaurant = torch.tensor([restaurant_id])

    with torch.no_grad():
        score = model(user, restaurant)

    return score.item()


if __name__ == "__main__":

    s = predict(10, 5)

    print("Recommendation score:", s)