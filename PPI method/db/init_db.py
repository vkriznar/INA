import sqlite3
from sqlite3.dbapi2 import Connection, Cursor


def init_db(con: Connection, cur: Cursor):
    # Create tables
    gene_table_query = """
    CREATE TABLE gene (
        id integer primary key,
        symbol text,
        description text,
        cluster_id integer
    )"""
    cur.execute(gene_table_query)
    gene_interaction_query = """
    CREATE TABLE gene_interaction (
        id integer primary key,
        first_gene_id integer,
        second_gene_id integer,
        FOREIGN KEY (first_gene_id)
            REFERENCES gene (id)
        FOREIGN KEY (second_gene_id)
            REFERENCES gene (id)
    )"""
    cur.execute(gene_interaction_query)
    drg_table_query = """
    CREATE TABLE drug (
        id integer primary key,
        symbol text
    )"""
    cur.execute(drg_table_query)
    drug_gene_interaction_query = """
    CREATE TABLE drug_gene_interaction (
        id integer primary key,
        gene_id integer,
        drug_id integer,
        FOREIGN KEY (gene_id)
            REFERENCES gene (id)
        FOREIGN KEY (drug_id)
            REFERENCES drug (id)
    )"""
    cur.execute(drug_gene_interaction_query)

    # Save commit changes
    con.commit()
    con.close()


if __name__ == "__main__":
    con = sqlite3.connect("db/atherosclerosis.db")
    cur = con.cursor()

    init_db(con, cur)
