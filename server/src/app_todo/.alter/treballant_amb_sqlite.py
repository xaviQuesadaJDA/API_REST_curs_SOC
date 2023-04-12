#!/usr/bin/python3

import sqlite3

ruta_fitxer = "una_base_de_dades.bd"
conn = sqlite3.connect(ruta_fitxer)


def drop_tables():
    query = "DROP TABLE if exists tasques ;"
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()


def create_tables():
    query = """
    CREATE TABLE if not exists tasques (
        title text,
        done boolean
        );
    """
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    cursor.close()


def main():
    drop_tables()
    create_tables()

   
if __name__ == "__main__":
    main()