import sqlite3
from typing import List


def fill_db(path: str, constants: list):
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.executemany('''INSERT INTO constants VALUES (?, ?)''', constants)
    connection.commit()
    connection.close()
