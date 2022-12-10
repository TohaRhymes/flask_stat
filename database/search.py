import sqlite3
import typing
import re

from model.datamodels import Constant


def search_constant(phrase: str, path: str) -> Constant:
    connection = sqlite3.connect(path)
    connection.create_function("REGEXP", 2, lambda expr, item: re.compile(expr).search(item.lower()) is not None)
    cursor = connection.cursor()

    rows = list(cursor.execute(f'''SELECT * FROM constants WHERE constant_name = "{phrase}"'''))
    print(rows)
    data = Constant(*(rows[0]))
    return data
