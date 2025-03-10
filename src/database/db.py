import os
import sqlite3
from typing import Optional

folder_path = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(folder_path, exist_ok=True)

file = "./data/users.db"
connection = sqlite3.connect(file)
connection.row_factory = sqlite3.Row


def fetch(query: str, params: Optional[list] = []):
    cursor = connection.cursor()

    try:
        cursor.execute(query, params)
        return cursor.fetchall()
    finally:
        cursor.close()


def run(query: str, params: Optional[list] = []):
    cursor = connection.cursor()

    try:
        cursor.execute(query, params)
        connection.commit()
    finally:
        cursor.close()
