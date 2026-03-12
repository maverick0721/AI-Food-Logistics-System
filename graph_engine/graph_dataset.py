import torch
import networkx as nx


class GraphDataset:

    def __init__(self, graph):

        self.graph = graph

    def build(self):

        edges = []

        for u, v in self.graph.edges():

            edges.append([u, v])

        edge_index = torch.tensor(edges).t().contiguous()

        num_nodes = self.graph.number_of_nodes()

        x = torch.ones((num_nodes, 8))

        return x, edge_index