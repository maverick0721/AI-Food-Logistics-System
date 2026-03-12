import torch
from torch.utils.data import Dataset
import pandas as pd


class DemandDataset(Dataset):

    def __init__(self, path, window=24):

        df = pd.read_parquet(path)

        series = df["demand"].values

        self.X = []
        self.y = []

        for i in range(len(series) - window):

            self.X.append(series[i:i+window])
            self.y.append(series[i+window])

    def __len__(self):

        return len(self.X)

    def __getitem__(self, idx):

        x = torch.tensor(self.X[idx]).float()
        y = torch.tensor(self.y[idx]).float()

        return x, y