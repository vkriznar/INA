from analysis.analysis import NetworkAnalyzer
from db.db_converter import DbConverter
from db.db_handler import DbHandler
from scripts.pancreatic_cancer import insert_db_data, insert_ppi_to_db, map_genes_to_drugs
import networkx as nx


if __name__ == "__main__":
    db_handler = DbHandler("db/pancreatic-cancer.db")
    #insert_db_data(db_handler)
    #insert_ppi_to_db(db_handler)
    db_converter = DbConverter("db/pancreatic-cancer.db")
    # db_converter.convert_to_pajek()
    # analyzer = NetworkAnalyzer(db_handler, "pancreatic-cancer")
    # analyzer.save_subgraphs()
    # map_genes_to_drugs(db_handler)
    db_converter.convert_bipartite_to_gml()
