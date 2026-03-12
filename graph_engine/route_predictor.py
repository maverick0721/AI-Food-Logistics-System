import torch

from graph_engine.gnn_model import RoutingGNN


class RoutePredictor:

    def __init__(self, model_path):

        self.model = RoutingGNN()

        self.model.load_state_dict(torch.load(model_path))

        self.model.eval()

    def score_nodes(self, x, edge_index):

        with torch.no_grad():

            return self.model(x, edge_index)