import torch
from torch.utils.data import Dataset
import pandas as pd


class RecommendationDataset(Dataset):

    def __init__(self, path):

        df = pd.read_parquet(path)

        self.users = torch.tensor(df["user_id"].values)
        self.restaurants = torch.tensor(df["restaurant_id"].values)
        self.ratings = torch.tensor(df["rating"].values).float()

    def __len__(self):

        return len(self.users)

    def __getitem__(self, idx):

        return self.users[idx], self.restaurants[idx], self.ratings[idx]