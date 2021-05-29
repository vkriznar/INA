import sqlite3


# Class for database manipulation, when inserting into tables, include parameter None for autoincrement primary key
class DbHandler:

    def __init__(self, database: str):
        self.con = sqlite3.connect(database)
        self.cur = self.con.cursor()

    def get_all_genes(self):
        self.cur.execute("SELECT * FROM gene")
        return self.cur.fetchall()

    def get_by_symbol(self, gene_symbol):
        self.cur.execute("SELECT * FROM gene WHERE symbol=:symbol", {"symbol": gene_symbol})
        return self.cur.fetchone()

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
