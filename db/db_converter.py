import networkx as nx
from db.db_handler import DbHandler


class DbConverter:

    def __init__(self, database: str) -> None:
        self.db = DbHandler(database)
        self.filename = database.split("/")[1].split(".")[0]

    def convert_to_pajek(self):
        graph = nx.Graph()
        nodes = self.db.get_all_genes()

        for node in nodes:
            graph.add_node(node.symbol)

        interactions = self.db.get_all_interactions()
        for interaction in interactions:
            graph.add_edge(interaction.gene1.symbol, interaction.gene2.symbol)

        nx.write_pajek(graph, f"analysis/data/{self.filename}/{self.filename}.net")
