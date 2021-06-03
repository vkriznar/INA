from db.db_handler import DbHandler
import networkx as nx
from cdlib.classes.node_clustering import NodeClustering
from cdlib.algorithms import louvain, walktrap


class NetworkAnalyzer:
    db_handler: DbHandler
    filename: str
    g: nx.Graph

    def __init__(self, db_handler: DbHandler, filename: str) -> None:
        self.db_handler = db_handler
        self.filename = filename
        self.g = nx.read_pajek(f"analysis/data/{filename}/{filename}.net")

    def get_communities(self) -> NodeClustering:
        return walktrap(self.g)

    def save_subgraphs(self):
        comms = self.get_communities()
        for i, comm in enumerate(comms.communities):
            if i > 6: return
            subg: nx.Graph = self.g.subgraph(comm)
            # nx.write_gml(subg, f"analysis/data/{self.filename}/{self.filename}_sub_{i+1}.gml")
            for node in subg.nodes:
                gene = self.db_handler.get_by_symbol(node)
                self.db_handler.set_gene_cluster(gene.id, i)
