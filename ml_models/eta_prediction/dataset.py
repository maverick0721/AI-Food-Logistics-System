import torch
from torch.utils.data import Dataset
import pandas as pd


class ETADataset(Dataset):

    def __init__(self, path):

        df = pd.read_parquet(path)

        self.X = df[
            ["distance", "traffic", "prep_time", "driver_load"]
        ].values

        self.y = df["eta"].values

    def __len__(self):

        return len(self.X)

    def __getitem__(self, idx):

        x = torch.tensor(self.X[idx]).float()
        y = torch.tensor(self.y[idx]).float()

        return x, y