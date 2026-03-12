import torch
import torch.nn as nn


class DemandTransformer(nn.Module):

    def __init__(self):

        super().__init__()

        self.embedding = nn.Linear(1, 64)

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=64,
            nhead=4
        )

        self.transformer = nn.TransformerEncoder(
            encoder_layer,
            num_layers=2
        )

        self.fc = nn.Linear(64, 1)

    def forward(self, x):

        x = x.unsqueeze(-1)

        x = self.embedding(x)

        x = self.transformer(x)

        x = x.mean(dim=1)

        return self.fc(x)