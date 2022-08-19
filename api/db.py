import sys
import sqlite3
from config import db_config
from sqlite3 import Error


class DatabaseWrapper:
    def __init__(self):
        self._db_file = db_config["db_file"]
        self._schema = db_config["schema_location"]
        self.conn = self._connect_to_db()

        # Make sure database schema is correct
        self._create_db()


    def _connect_to_db(self):
        try:
            conn = sqlite3.connect(self._db_file, check_same_thread=False)
            conn.row_factory = sqlite3.Row

            return conn
        except Error as e:
            print(f"{e}\n\nFatal Error occured: Unable to connect to database. Quitting ...")
            sys.exit(1)


    def _create_db(self):
        if self._schema != "":
            with open(self._schema, "r") as f:
                schema = f.read()
                self.conn.executescript(schema)


    def _list_and_dictify(self, items, one=False):
        if items is None:
            return None
        
        elif one:
            return dict(items)

        new_list = []
        for row in items:
            new_list.append(dict(row))

        return new_list