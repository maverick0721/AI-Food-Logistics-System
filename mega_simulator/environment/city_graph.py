import osmnx as ox
import networkx as nx


class CityGraph:

    def __init__(self, city_name):

        self.graph = ox.graph_from_place(city_name, network_type="drive")

    def shortest_path(self, a, b):

        return nx.shortest_path(self.graph, a, b, weight="length")

    def distance(self, a, b):

        return nx.shortest_path_length(self.graph, a, b, weight="length")