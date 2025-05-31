import sqlite3
import os
from utils.path_helper import resource_path

DB_NAME = resource_path("barangay.db")

def init_db():
    os.makedirs(os.path.dirname(DB_NAME), exist_ok=True)

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS residents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                age INTEGER,
                address TEXT,
                contact TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                resident_id INTEGER NOT NULL,
                document_type TEXT NOT NULL,
                purpose TEXT,
                status TEXT DEFAULT 'Pending',
                request_date TEXT NOT NULL,
                FOREIGN KEY (resident_id) REFERENCES residents(id)
            )
        """)

        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[ERROR] Failed to init DB: {e}")

def get_count(table, condition=None):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        query = f"SELECT COUNT(*) FROM {table}"
        if condition:
            query += f" WHERE {condition}"
        cursor.execute(query)
        count = cursor.fetchone()[0]
        conn.close()
        return count
    except Exception as e:
        print(f"Database error: {e}")
        return "N/A"
