from db.db_handler import DbHandler
from scripts.pancreatic_cancer import insert_db_data, insert_ppi_to_db


if __name__ == "__main__":
    db_handler = DbHandler("db/pancreatic-cancer.db")
    insert_db_data(db_handler)
    insert_ppi_to_db(db_handler)
