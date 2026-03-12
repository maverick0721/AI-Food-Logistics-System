import torch
from torch.utils.data import DataLoader

from ml_models.demand_forecasting.dataset import DemandDataset
from ml_models.demand_forecasting.model import DemandTransformer


def train():

    dataset = DemandDataset("datasets/raw/demand_timeseries.parquet")

    loader = DataLoader(dataset, batch_size=128, shuffle=True)

    model = DemandTransformer()

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

    torch.save(model.state_dict(), "models/demand_model.pt")


if __name__ == "__main__":

    train()