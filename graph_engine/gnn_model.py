import torch
import torch.nn as nn
from torch_geometric.nn import GCNConv


class RoutingGNN(nn.Module):

    def __init__(self):

        super().__init__()

        self.conv1 = GCNConv(8, 32)

        self.conv2 = GCNConv(32, 32)

        self.fc = nn.Linear(32, 1)

    def forward(self, x, edge_index):

        x = self.conv1(x, edge_index)

        x = torch.relu(x)

        x = self.conv2(x, edge_index)

        x = torch.relu(x)

        return self.fc(x)