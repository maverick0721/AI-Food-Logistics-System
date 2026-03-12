import torch
from torch.utils.data import DataLoader

from ml_models.recommendation.dataset import RecommendationDataset
from ml_models.recommendation.model import TwoTowerModel


def train():

    dataset = RecommendationDataset(
        "datasets/raw/recommendation_data.parquet"
    )

    loader = DataLoader(dataset, batch_size=256, shuffle=True)

    model = TwoTowerModel()

    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    loss_fn = torch.nn.MSELoss()

    for epoch in range(10):

        total_loss = 0

        for user, restaurant, rating in loader:

            pred = model(user, restaurant)

            loss = loss_fn(pred, rating)

            optimizer.zero_grad()

            loss.backward()

            optimizer.step()

            total_loss += loss.item()

        print("Epoch", epoch, "Loss", total_loss)

    torch.save(model.state_dict(), "models/recommendation_model.pt")

    print("Model saved")


if __name__ == "__main__":

    train()