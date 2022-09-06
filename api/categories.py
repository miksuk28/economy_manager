from db import DatabaseWrapper
import sqlite3
import eco_exceptions as exc

class Categories(DatabaseWrapper):
    def __init__(self):
        DatabaseWrapper.__init__(self)

    
    def get_categories(self):
        cur = self.conn.cursor()
        cur.execute(
            '''
            SELECT id, name FROM categories
            '''
        )
        categories = self._list_and_dictify(cur.fetchall())

        return categories


    def _register_category(self, name):
        cur = self.conn.cursor()
        cur.execute(
            '''
            INSERT INTO categories (name)
            VALUES (?)
            ''',
            (name,)
        )
        self.conn.commit()
        return cur.lastrowid


    def create_category(self, name, raise_if_exists=False):
        cur = self.conn.cursor()
        cur.execute(
            '''
            SELECT id, name
            FROM categories
            WHERE name=?
            ''',
            (name,)
        )
        result = cur.fetchone()
        if result is not None:
            return result["id"], True

        return self._register_category(name), False