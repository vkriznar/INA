from analysis.analysis import NetworkAnalyzer
from db.db_converter import DbConverter
from db.db_handler import DbHandler
from scripts.scripts import insert_db_data, insert_ppi_to_db, map_genes_to_drugs
import networkx as nx


if __name__ == "__main__":
    db_handler = DbHandler("db/prostate-cancer.db")
    drug_degree_pairs = db_handler.get_drug_degrees()
    print(sorted(drug_degree_pairs, key=lambda x: x[1], reverse=True)[:10])

    # db_handler = DbHandler("db/atherosclerosis.db")
    # insert_db_data(db_handler, "atherosclerosis")
    # insert_ppi_to_db(db_handler)
    # db_converter = DbConverter("db/atherosclerosis.db")
    # db_converter.convert_to_pajek()
    # db_converter.convert_to_gml()
    # analyzer = NetworkAnalyzer(db_handler, "atherosclerosis")
    # analyzer.save_subgraphs()
    # map_genes_to_drugs(db_handler)
    # db_converter.convert_bipartite_to_gml()
