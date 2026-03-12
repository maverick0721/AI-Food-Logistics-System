import torch

from graph_engine.graph_builder import GraphBuilder
from graph_engine.graph_dataset import GraphDataset
from graph_engine.gnn_model import RoutingGNN


def train():

    builder = GraphBuilder("Roorkee")

    graph = builder.build()

    dataset = GraphDataset(graph)

    x, edge_index = dataset.build()

    model = RoutingGNN()

    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    for epoch in range(20):

        pred = model(x, edge_index)

        loss = pred.mean()

        optimizer.zero_grad()

        loss.backward()

        optimizer.step()

        print("Epoch", epoch, "Loss", loss.item())


if __name__ == "__main__":

    train()