from schemas.schemas import Gene, GeneInteraction
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

    def get_by_symbol(self, gene_symbol):
        self.cur.execute("SELECT * FROM gene WHERE symbol=:symbol", {"symbol": gene_symbol})
        return self._map_gene(self.cur.fetchone())

    def create_gene(self, symbol, description):
        self.cur.execute("INSERT INTO gene values (?, ?, ?)", (None, symbol, description))
        self.con.commit()
        return self.cur.lastrowid

    def interact(self, gene1_id: int, gene2_id: int) -> bool:
        query = """
            SELECT 1 FROM gene_interaction
            WHERE (first_gene_id=:g1 AND second_gene_id=:g2)
            OR (first_gene_id=:g2 AND second_gene_id=:g1)
        """
        self.cur.execute(query, {"g1": gene1_id, "g2": gene2_id})
        return self.cur.fetchone() is not None

    def create_interaction(self, gene1_id: int, gene2_id: int):
        self.cur.execute("INSERT INTO gene_interaction values (?, ?, ?)", (None, gene1_id, gene2_id))
        self.con.commit()
        return self.cur.lastrowid

    def get_all_interactions(self):
        self.cur.execute("SELECT * FROM gene_interaction")
        return list(map(lambda i: self._map_interaction(i), self.cur.fetchall()))

    def get_all_interactions_by_gene(self, gene_id: int):
        query = "SELECT * FROM gene_interaction WHERE first_gene_id=:gene_id OR gene_interaction WHERE second_gene_id=:gene_id"
        return list(map(lambda i: self._map_interaction(i), self.cur.execute(query, {"gene_id": gene_id})))

    def _map_gene(self, gene):
        return None if gene is None else Gene(gene[0], gene[1], gene[2])

    def _map_interaction(self, interaction):
        gene1 = self.get(interaction[1])
        gene2 = self.get(interaction[2])

        return GeneInteraction(interaction[0], gene1, gene2)
