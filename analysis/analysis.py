from cdlib.classes.node_clustering import NodeClustering
import networkx as nx
import matplotlib.pyplot as plt
from cdlib.algorithms import louvain


class NetworkAnalyzer:
    g: nx.Graph
    comms: NodeClustering

    def __init__(self, filename: str) -> None:
        self.g = nx.read_pajek(f"analysis/data/{filename}.net")

    def get_communities(self):
        self.comms = louvain(self.g)
        return self.comms

    def draw_subgraph(self, nodes):
        subgraph = self.g.subgraph(nodes)
        nx.draw(subgraph, with_labels=True, pos=nx.spring_layout(subgraph))
        plt.show()
