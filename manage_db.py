import sqlite3
from os import getenv
from sys import argv

from dotenv import load_dotenv

from web_scrapper import get_data_name

load_dotenv()


class Database:
    def __init__(self, db_name: str) -> None:
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        self.cursor = self.connection.cursor()
        self.table_db = getenv('DB_TABLE')

    def __del__(self) -> None:
        self.connection.close()

    def create_table(self, sql_request: str) -> None:
        self.cursor.execute(sql_request)
        self.connection.commit()

    def insert(self, *values) -> None:
        self.cursor.execute(f"INSERT INTO {self.table_db}  VALUES({','.join(['?' for _ in values])})", values)
        self.connection.commit()

    def fetch_all(self) -> list:
        self.cursor.execute(f"SELECT rowid, * FROM {self.table_db}")
        names = self.cursor.fetchall()
        return names

    def get_just_list_name(self) -> list:
        list_name = []
        for name in self.fetch_all():
            list_name.append(name[1])
        return list_name

    def get_dict_names(self) -> dict:
        fetched_names = self.fetch_all()
        dict_of_names = dict((id_name, name) for id_name, name, origin, meaning in fetched_names)
        return dict_of_names

    def get_name_by_id(self, row_id: int) -> str:
        self.cursor.execute(f"SELECT * FROM {self.table_db} WHERE rowid = {row_id}")
        name = self.cursor.fetchone()
        return name

    def get_name_row_by_value(self, name_value: str) -> str:
        self.cursor.execute(f"SELECT * FROM {self.table_db} WHERE name = '{name_value}'")
        name = self.cursor.fetchone()
        return name

    def get_specific_amount_of_names(self, limiter: int) -> list:
        list_of_names = []
        self.cursor.execute(f"SELECT * FROM {self.table_db} WHERE rowid >= {limiter}")
        names = self.cursor.fetchmany(limiter)
        for name in names:
            list_of_names.append(name[0])
        return list_of_names if limiter > 0 else f"You wanted 0, so you got it :)"

    def delete_item(self, table) -> None:
        self.cursor.execute(f"DELETE FROM {table}")
        self.connection.commit()


def manage() -> None:
    """Here are the methods which allow you to manage database and
       execute SQLite requests. """
    db = Database(getenv("DATABASE"))

    if len(argv) > 1 and argv[1] == "--setup":
        db.create_table(f"CREATE TABLE {db.table_db} (name text, origin text, meaning text)")
        print(f"DB table {db.table_db} has been created")

    if len(argv) > 1 and argv[1] == "--add-names":
        """
        Usage: python manage_db.py --add-names (values: 1. name 2. origin_name 3. meaning_name)
        """
        for el in get_data_name():
            name = el['name']
            origin = el['origin_name']
            meaning = el['meaning_name']
            db.insert(name, origin, meaning)

    if len(argv) > 1 and argv[1] == "--show-all-names":
        content_db = db.fetch_all()
        print(content_db)

    if len(argv) > 1 and argv[1] == "--show-dict-names":
        print(db.get_dict_names())

    if len(argv) > 1 and argv[1] == "--show":
        print(db.get_name_by_id(3))

    if len(argv) > 1 and argv[1] == "--amount":
        print(db.get_specific_amount_of_names(1))

    if len(argv) > 1 and argv[1] == "--list-name":
        print(db.get_just_list_name())

    if len(argv) > 1 and argv[1] == "--get-row":
        print(db.get_name_row_by_value('Ada'))

    if len(argv) > 1 and argv[1] == "--delete":
        db.delete_item(db.table_db)
        if len(db.fetch_all()) < 1:
            print("Data base is empty.")


if __name__ == '__main__':
    manage()
