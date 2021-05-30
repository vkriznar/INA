import json
import requests
from time import sleep
from db.db_handler import DbHandler


def insert_db_data(db_handler: DbHandler):
    print("Started inserting pancreatic cancer genes into database")
    with open("scripts/data/cancer_category_rna_prostate.json") as f:
        data = json.load(f)
        for gene_obj in data:
            db_handler.create_gene(gene_obj["Gene"], gene_obj["Gene description"])
    print("Finished")


def insert_ppi_to_db(db_handler: DbHandler):
    print("Started mapping protein-protein interaction network to db")
    data = db_handler.get_all_genes()
    for i, gene in enumerate(data):
        print(f"Mapping protein interaction for gene {gene.symbol} [{i}/{len(data)}]")
        sleep(1)
        response = requests.get(f"https://string-db.org/api/json/network?identifiers={gene.symbol}")
        response_data = json.loads(response.content.decode("utf-8"))
        if response.status_code != 200:
            continue
        for interaction in response_data:
            gene_symbol_a = interaction["preferredName_A"]
            gene_symbol_b = interaction["preferredName_B"]

            gene_a_id = _get_gene_id_or_create(db_handler, gene_symbol_a)
            gene_b_id = _get_gene_id_or_create(db_handler, gene_symbol_b)

            if not db_handler.interact(gene_a_id, gene_b_id):
                db_handler.create_interaction(gene_a_id, gene_b_id)

    print("Finished")


def _get_gene_id_or_create(db_handler: DbHandler, gene_symbol: str):
    gene_db_a = db_handler.get_by_symbol(gene_symbol)
    if gene_db_a is None:
        print(f"Adding gene {gene_symbol} into database")
        return db_handler.create_gene(gene_symbol, "Added from interaction")
    return gene_db_a.id
