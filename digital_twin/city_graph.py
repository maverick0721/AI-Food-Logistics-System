import osmnx as ox
import networkx as nx


class CityGraph:

    def __init__(self, city):

        self.city = city

    def build(self):

        graph = ox.graph_from_place(self.city, network_type="drive")

        graph = nx.convert_node_labels_to_integers(graph)

        return graph