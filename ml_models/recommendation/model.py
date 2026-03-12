import torch
import torch.nn as nn


class TwoTowerModel(nn.Module):

    def __init__(self, num_users=500, num_restaurants=200, embedding_dim=32):

        super().__init__()

        self.user_embedding = nn.Embedding(num_users, embedding_dim)
        self.restaurant_embedding = nn.Embedding(num_restaurants, embedding_dim)

        self.fc = nn.Linear(embedding_dim, 1)

    def forward(self, user, restaurant):

        u = self.user_embedding(user)
        r = self.restaurant_embedding(restaurant)

        x = u * r

        return self.fc(x).squeeze()