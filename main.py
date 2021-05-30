from analysis.analysis import NetworkAnalyzer
from db.db_converter import DbConverter
from db.db_handler import DbHandler
from scripts.pancreatic_cancer import insert_db_data, insert_ppi_to_db


if __name__ == "__main__":
    db_handler = DbHandler("db/pancreatic-cancer.db")
    # insert_db_data(db_handler)
    # insert_ppi_to_db(db_handler)
    db_converter = DbConverter("db/pancreatic-cancer.db")
    # db_converter.convert_to_pajek()
    analyzer = NetworkAnalyzer("pancreatic-cancer")
    comms = analyzer.get_communities()

    comm1 = analyzer.g.subgraph(comms.communities[10])
    analyzer.draw_subgraph(comm1)
