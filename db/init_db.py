import sqlite3
from sqlite3.dbapi2 import Connection, Cursor


def init_db(con: Connection, cur: Cursor):
    # Create tables
    gene_table_query = "CREATE TABLE gene (id integer primary key, symbol text, description text)"
    cur.execute(gene_table_query)
    gene_interaction_query = "CREATE TABLE gene_interaction (id integer primary key, first_gene_id integer, second_gene_id integer)"
    cur.execute(gene_interaction_query)

    # Save commit changes
    con.commit()
    con.close()


if __name__ == "__main__":
    con = sqlite3.connect("db/pancreatic-cancer.db")
    cur = con.cursor()

    init_db(con, cur)
