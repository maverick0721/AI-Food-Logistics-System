import torch

from ml_models.eta_prediction.model import ETAModel


def predict(distance, traffic, prep_time, driver_load):

    model = ETAModel()

    model.load_state_dict(torch.load("models/eta_model.pt"))

    x = torch.tensor(
        [[distance, traffic, prep_time, driver_load]]
    ).float()

    eta = model(x)

    return eta.item()


if __name__ == "__main__":

    eta = predict(5, 3, 10, 2)

    print("Predicted ETA:", eta)