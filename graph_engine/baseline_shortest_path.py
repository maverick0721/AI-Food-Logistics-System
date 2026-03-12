import networkx as nx


def shortest_path(graph, source, target):

    return nx.shortest_path(graph, source, target, weight="length")