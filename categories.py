from db import DatabaseWrapper
import sqlite3
import eco_exceptions as exc

class Categories(DatabaseWrapper):
    def __init__(self):
        DatabaseWrapper.__init__(self)

    
    def get_categories(self, username):
        cur = self.conn.cursor()
        cur.execute(
            '''
            SELECT id, name FROM categories
            WHERE user_id=(SELECT id FROM users WHERE username=?)
            ''',
            (username,)
        )
        categories = self._list_and_dictify(cur.fetchall())

        return categories


    def _register_category(self, username, name):
        cur = self.conn.cursor()
        cur.execute(
            '''
            INSERT INTO categories (user_id, name)
            VALUES ((SELECT id FROM users WHERE username=?),?)
            ''',
            (username, name)
        )
        self.conn.commit()
        return cur.lastrowid


    def create_category(self, username, name, raise_if_exists=False):
        cur = self.conn.cursor()
        cur.execute(
            '''
            SELECT id, name
            FROM categories
            WHERE name=? AND
            user_id=(SELECT id FROM users WHERE username=?)
            ''',
            (name, username)
        )
        result = cur.fetchone()
        if result is not None:
            return result["id"], True

        return self._register_category(username, name), False