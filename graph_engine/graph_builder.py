import osmnx as ox
import networkx as nx


class GraphBuilder:

    def __init__(self, city, dist=5000):

        self.city = city
        self.dist = dist

    def build(self):

        try:
            graph = ox.graph_from_place(self.city, network_type="drive")
        except TypeError:
            center = ox.geocode(self.city)
            graph = ox.graph_from_point(center, dist=self.dist, network_type="drive")

        graph = nx.convert_node_labels_to_integers(graph)

        return graph