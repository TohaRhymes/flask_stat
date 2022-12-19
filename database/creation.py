import sqlite3


def create_db(path: str, constant_names: list):
    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    constant_names_string = "'" + "','".join(constant_names) + "'"

    cursor.execute("""DROP TABLE IF EXISTS constants""")
    cursor.execute(f"""CREATE TABLE constants (
    constant_name TEXT CHECK( constant_name IN ({constant_names_string}) ), 
    constant_value NOT NULL)""")

    connection.commit()
    connection.close()
