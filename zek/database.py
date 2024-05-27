# database.py
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_db_connection_t():
    conn = sqlite3.connect('regis.db')
    conn.row_factory = sqlite3.Row
    return conn
