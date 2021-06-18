import networkx as nx
from networkx.algorithms import bipartite
from networkx.algorithms.bipartite.basic import degrees
from db.db_handler import DbHandler


class DbConverter:

    def __init__(self, database: str) -> None:
        self.db = DbHandler(database)
        self.filename = database.split("/")[1].split(".")[0]

    def create_graph(self):
        graph = nx.Graph()
        nodes = self.db.get_all_genes()

        for node in nodes:
            graph.add_node(node.symbol)

        interactions = self.db.get_all_interactions()
        for interaction in interactions:
            graph.add_edge(interaction.gene1.symbol, interaction.gene2.symbol)

        return graph

    def convert_to_pajek(self):
        graph = self.create_graph()
        nx.write_pajek(graph, f"analysis/data/{self.filename}/{self.filename}.net")

    def convert_to_gml(self):
        graph = self.create_graph()
        nx.write_gml(graph, f"analysis/data/{self.filename}/{self.filename}.gml")

    def convert_bipartite_to_gml(self):
        graph = nx.Graph()

        genes = list(map(lambda g: g.symbol, self.db.get_all_genes_with_cluster()))
        graph.add_nodes_from(genes, bipartite=0, degree=2)
        interactions = self.db.get_all_interactions()
        for interaction in interactions:
            if interaction.gene1.cluster_id is not None and interaction.gene2.cluster_id is not None:
                graph.add_edge(interaction.gene1.symbol, interaction.gene2.symbol)

        drug_degree_pairs = self.db.get_drug_degrees()
        for drug_degree_pair in drug_degree_pairs:
            graph.add_node(drug_degree_pair[0], bipartite=1, degree=drug_degree_pair[1])
        gd_interactions = self.db.get_all_gd_interactions()
        for gd_interaction in gd_interactions:
            graph.add_edge(gd_interaction.gene.symbol, gd_interaction.drug.symbol)

        print(sorted(drug_degree_pairs, key=lambda x: x[1], reverse=True)[:10])

        nx.write_gml(graph, f"analysis/data/{self.filename}/{self.filename}-bipartite.gml")
