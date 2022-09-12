import eco_exceptions as exc
import hashlib
import auth_exceptions as auth_exc
import secrets
from db import DatabaseWrapper
from bcrypt import gensalt
from hmac import compare_digest


class Authentication(DatabaseWrapper):
    def __init__(self):
        DatabaseWrapper.__init__(self)
        self.sessions = {}


    def _hash_password(self, password, salt):
        hashed = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            100000
        )

        return hashed.hex()


    def get_user_id(self, username):
        cur = self.conn.cursor()
        cur.execute(
            '''
            SELECT id FROM users
            WHERE username=?
            ''',
            (username,)
        )
        result = cur.fetchone()
        
        if result is None:
            return None

        return result["id"]

    
    def _set_password(self, user_id, password):
        # Delete old password first
        cur = self.conn.cursor()
        cur.execute(
            '''
            DELETE FROM passwords
            WHERE user_id=?
            ''',
            (user_id,)
        )
        
        salt = gensalt().hex()
        hashed_password = self._hash_password(password, salt)

        cur.execute(
            '''
            INSERT INTO passwords (user_id,hashed,salt)
            VALUES (?,?,?)
            ''',
            (user_id, hashed_password, salt)
        )
        self.conn.commit()


    def _getpass(self, username):
        cur = self.conn.cursor()
        cur.execute(
            '''
            SELECT hashed, salt
            FROM passwords
            WHERE user
            '''
        )


    def login(self, username, password):
        if self.get_user_id(username) is None:
            raise auth_exc.UserDoesNotExist()(username)




    def create_user(self, username, password, fname=None, lname=None, logon_allowed=True):
        if self.get_user_id(username) is not None:
            raise auth_exc.UserAlreadyExists(username)

        cur = self.conn.cursor()
        cur.execute(
            '''
            INSERT INTO users (username,fname,lname,logon_allowed)
            VALUES (?,?,?,?)
            ''',
            (username, fname, lname, logon_allowed)
        )
        self.conn.commit()

        user_id = cur.lastrowid
        self._set_password(user_id, password)

        return user_id