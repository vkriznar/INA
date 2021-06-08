from typing import Union
from schemas.schemas import Drug, Gene, GeneDrugInteraction, GeneInteraction
import sqlite3


# Class for database manipulation, when inserting into tables, include parameter None for autoincrement primary key
class DbHandler:

    def __init__(self, database: str):
        self.con = sqlite3.connect(database)
        self.cur = self.con.cursor()

    def get(self, gene_id):
        self.cur.execute("SELECT * FROM gene WHERE id=:gene_id", {"gene_id": gene_id})
        return self._map_gene(self.cur.fetchone())

    def get_all_genes(self):
        self.cur.execute("SELECT * FROM gene")
        return list(map(lambda g: self._map_gene(g), self.cur.fetchall()))

    def get_all_genes_with_cluster(self):
        self.cur.execute("SELECT * FROM gene WHERE cluster_id IS NOT NULL")
        return list(map(lambda g: self._map_gene(g), self.cur.fetchall()))

    def get_by_symbol(self, gene_symbol: str):
        self.cur.execute("SELECT * FROM gene WHERE symbol=:symbol", {"symbol": gene_symbol})
        return self._map_gene(self.cur.fetchone())

    def create_gene(self, symbol: str, description: str):
        self.cur.execute("INSERT INTO gene VALUES (?, ?, ?, ?)", (None, symbol, description, None))
        self.con.commit()
        return self.cur.lastrowid

    def set_gene_cluster(self, gene_id: int, cluster_id: int):
        self.cur.execute("UPDATE gene SET cluster_id=:cluster_id WHERE id=:gene_id", {"cluster_id": cluster_id, "gene_id": gene_id})
        self.con.commit()

    def interact(self, gene1_id: int, gene2_id: int) -> bool:
        query = """
            SELECT 1 FROM gene_interaction
            WHERE (first_gene_id=:g1 AND second_gene_id=:g2)
            OR (first_gene_id=:g2 AND second_gene_id=:g1)
        """
        self.cur.execute(query, {"g1": gene1_id, "g2": gene2_id})
        return self.cur.fetchone() is not None

    def create_interaction(self, gene1_id: int, gene2_id: int):
        self.cur.execute("INSERT INTO gene_interaction VALUES (?, ?, ?)", (None, gene1_id, gene2_id))
        self.con.commit()
        return self.cur.lastrowid

    def get_all_interactions(self):
        self.cur.execute("SELECT * FROM gene_interaction")
        return list(map(lambda i: self._map_interaction(i), self.cur.fetchall()))

    def get_all_interactions_by_gene(self, gene_id: int):
        query = "SELECT * FROM gene_interaction WHERE first_gene_id=:gene_id OR gene_interaction WHERE second_gene_id=:gene_id"
        return list(map(lambda i: self._map_interaction(i), self.cur.execute(query, {"gene_id": gene_id})))

    def get_drug(self, drug_id):
        self.cur.execute("SELECT * FROM drug WHERE id=:drug_id", {"drug_id": drug_id})
        return self._map_drug(self.cur.fetchone())

    def get_drug_by_symbol(self, symbol: str):
        self.cur.execute("SELECT * FROM drug WHERE symbol=:symbol", {"symbol": symbol})
        return self._map_drug(self.cur.fetchone())

    def get_all_drugs(self):
        self.cur.execute("SELECT * FROM drug")
        return list(map(lambda d: self._map_drug(d), self.cur.fetchall()))

    def create_drug(self, symbol: str):
        self.cur.execute("INSERT INTO drug VALUES (?, ?)", (None, symbol))
        self.con.commit()
        return self.cur.lastrowid

    def get_all_gd_interactions(self):
        self.cur.execute("SELECT * FROM drug_gene_interaction")
        return list(map(lambda i: self._map_gd_interaction(i), self.cur.fetchall()))

    def create_gd_interaction(self, gene_id: int, drug_id: int):
        self.cur.execute("INSERT INTO drug_gene_interaction VALUES (?, ?, ?)", (None, gene_id, drug_id))
        self.con.commit()
        return self.cur.lastrowid

    def gene_drug_interact(self, gene_id: int, drug_id: int) -> bool:
        query = "SELECT 1 FROM drug_gene_interaction WHERE (gene_id=:gene_id AND drug_id=:drug_id)"
        self.cur.execute(query, {"gene_id": gene_id, "drug_id": drug_id})
        return self.cur.fetchone() is not None

    def get_drug_degrees(self):
        query = "SELECT drug_id, count(*) FROM drug_gene_interaction GROUP BY drug_id"
        self.cur.execute(query)
        return list(map(lambda i: self._map_drug_degree(i), self.cur.fetchall()))

    def _map_gene(self, gene):
        return None if gene is None else Gene(gene[0], gene[1], gene[2], gene[3])

    def _map_drug(self, drug):
        return None if drug is None else Drug(drug[0], drug[1])

    def _map_interaction(self, interaction):
        gene1 = self.get(interaction[1])
        gene2 = self.get(interaction[2])

        if gene1 is None or gene2 is None:
            raise Exception

        return GeneInteraction(interaction[0], gene1, gene2)

    def _map_gd_interaction(self, interaction):
        gene = self.get(interaction[1])
        drug = self.get_drug(interaction[2])

        if gene is None or drug is None:
            raise Exception

        return GeneDrugInteraction(interaction[0], gene, drug)

    def _map_drug_degree(self, degree_pair):
        drug = self.get_drug(degree_pair[0])
        return (drug.symbol, degree_pair[1])
