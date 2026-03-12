import torch
import torch.nn as nn


class LogisticsTransformer(nn.Module):

    def __init__(self, vocab_size=100):

        super().__init__()

        self.embedding = nn.Embedding(vocab_size, 256)

        encoder_layer = nn.TransformerEncoderLayer(

            d_model=256,
            nhead=8

        )

        self.transformer = nn.TransformerEncoder(

            encoder_layer,
            num_layers=6

        )

        self.head = nn.Linear(256, vocab_size)

    def forward(self, x):

        x = self.embedding(x)

        x = self.transformer(x)

        return self.head(x)