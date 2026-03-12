import torch

from ml_models.demand_forecasting.model import DemandTransformer


def predict(window):

    model = DemandTransformer()

    model.load_state_dict(torch.load("models/demand_model.pt"))

    x = torch.tensor(window).float().unsqueeze(0)

    pred = model(x)

    return pred.item()


if __name__ == "__main__":

    window = [100]*24

    forecast = predict(window)

    print("Predicted demand:", forecast)