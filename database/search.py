import sqlite3
import re

from model.datamodels import Constant


def search_constant(phrase: str, path: str):
    connection = sqlite3.connect(path)
    connection.create_function("REGEXP", 2, lambda expr, item: re.compile(expr).search(item.lower()) is not None)
    cursor = connection.cursor()

    rows = list(cursor.execute(f'''SELECT * FROM constants WHERE constant_name = "{phrase}"'''))
    data = Constant(*(rows[0]))
    return data.constant_value
