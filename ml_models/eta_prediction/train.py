import torch
from torch.utils.data import DataLoader

from ml_models.eta_prediction.dataset import ETADataset
from ml_models.eta_prediction.model import ETAModel


def train():

    dataset = ETADataset("datasets/features/orders_features.parquet")

    loader = DataLoader(dataset, batch_size=256, shuffle=True)

    model = ETAModel()

    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    loss_fn = torch.nn.MSELoss()

    for epoch in range(10):

        total_loss = 0

        for x, y in loader:

            pred = model(x).squeeze()

            loss = loss_fn(pred, y)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        print("Epoch", epoch, "Loss", total_loss)

    torch.save(model.state_dict(), "models/eta_model.pt")


if __name__ == "__main__":

    train()