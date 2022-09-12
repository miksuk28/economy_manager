import eco_exceptions as exc
import hashlib
import auth_exceptions as auth_exc
import secrets
from datetime import datetime, timedelta
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
            SELECT id, logon_allowed
            FROM users
            WHERE username=?
            ''',
            (username,)
        )
        result = cur.fetchone()
        
        if result is None:
            return None

        return dict(result)

    
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
            SELECT users.username,hashed,salt
            FROM passwords
            JOIN users ON passwords.user_id=users.id
            WHERE username=?
            ''',
            (username,)
        )
        result = cur.fetchone()
        return dict(result)


    def login(self, username, password):
        user_info = self.get_user_id(username)
        if user_info is None:
            raise auth_exc.UserDoesNotExist()(username)
        
        elif not user_info["logon_allowed"]:
            raise auth_exc.LoginBlocked(username)

        # Get correct creds from db
        creds = self._getpass(username)
        # Hash supplied password
        hashed_password = self._hash_password(
            password,
            creds["salt"]
        )
        # Check password
        if not compare_digest(hashed_password, creds["hashed"]):
            raise auth_exc.IncorrectPassword(username)
        else:
            auth_token = secrets.token_urlsafe(48)
            session = self._register_token(user_id=user_info["id"], token=auth_token)

            return session


    def _register_token(self, user_id, token):
        exp = datetime.utcnow() + timedelta(hours=24)
        exp = exp.strftime("%Y-%m-%d %H:%M")

        cur = self.conn.cursor()
        cur.execute(
            '''
            INSERT INTO sessions (user_id,token,expiration)
            VALUES (?,?,?)
            ''',
            (user_id, token, exp)
        )
        self.conn.commit()
        return {"token": token, "exp": exp, "id": user_id}


    def auth(self, token):
        cur = self.conn.cursor()
        cur.execute(
            '''
            SELECT users.username, token, expiration AS exp, user_id
            FROM sessions
            JOIN users ON sessions.user_id=users.id
            WHERE token=?
            ''',
            (token,)
        )
        session = cur.fetchone()

        if session is None:
            raise auth_exc.InvalidToken()

        exp = datetime.strptime(session["exp"], "%Y-%m-%d %H:%M")
        if exp <= datetime.utcnow():
            raise auth_exc.TokenExpired()

        return dict(session)



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