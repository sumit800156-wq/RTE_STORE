import sqlite3

DATABASE_NAME = "rte_store.db"

def get_connection():
    return sqlite3.connect(DATABASE_NAME)