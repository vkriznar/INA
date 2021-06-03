import json
from schemas.schemas import Drug, Gene
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

            gene_a_id = _get_gene_or_create(db_handler, gene_symbol_a)
            gene_b_id = _get_gene_or_create(db_handler, gene_symbol_b)

            if not db_handler.interact(gene_a_id, gene_b_id):
                db_handler.create_interaction(gene_a_id, gene_b_id)

    print("Finished")


def map_genes_to_drugs(db_handler: DbHandler):
    print("Started mapping protein-drug interaction network to db")

    data = db_handler.get_all_genes_with_cluster()
    genes = list(map(lambda g: g.symbol, data))

    for i in range(0, len(genes), 10):
        print(f"Running batch number [{int(i/10)+1}/{int(len(genes)/10)+1}]")
        genes_batch = genes[i:i+10]

        response = requests.get(f"https://dgidb.org/api/v2/interactions.json?genes={','.join(genes_batch)}&fda_approved_drug=true")
        response_data = json.loads(response.content.decode("utf-8"))

        if response.status_code != 200:
            raise Exception

        for gene_obj in response_data["matchedTerms"]:
            print(f"Mapping protein-drug interaction for gene: {gene_obj['geneName']}")
            gene = db_handler.get_by_symbol(gene_obj['searchTerm'])

            for interaction in gene_obj["interactions"]:
                if interaction["score"] < 0.8:
                    continue

                drug_symbol = interaction["drugName"]
                drug_id = _get_drug_or_create(db_handler, drug_symbol)

                if not db_handler.gene_drug_interact(gene.id, drug_id):
                    db_handler.create_gd_interaction(gene.id, drug_id)

    print("Finished")


def _get_gene_or_create(db_handler: DbHandler, gene_symbol: str) -> int:
    gene_db = db_handler.get_by_symbol(gene_symbol)
    if gene_db is None:
        print(f"Adding gene {gene_symbol} into database")
        return db_handler.create_gene(gene_symbol, "Added from interaction")
    return gene_db.id


def _get_drug_or_create(db_handler: DbHandler, drug_symbol: str) -> int:
    drug_db = db_handler.get_drug_by_symbol(drug_symbol)
    if drug_db is None:
        print(f"Adding drug {drug_symbol} into database")
        return db_handler.create_drug(drug_symbol)
    return drug_db.id
