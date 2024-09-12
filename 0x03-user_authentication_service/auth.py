#!/usr/bin/env python3
"""
auth
"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    '''hashing pswd'''
    # Convert the password string to bytes
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password


def _generate_uuid() -> str:
    '''return a string representation of a new UUID'''
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        '''init'''
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        '''registering a user'''
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pass_hashed = _hash_password(password)
            new_user = self._db.add_user(email=email,
                                         hashed_password=pass_hashed)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        '''validate user'''
        try:
            user = self._db.find_user_by(email=email)
            bytes_password = password.encode("utf-8")
            return bcrypt.checkpw(bytes_password, user.hashed_password)
        except Exception:
            return False

    def create_session(self, email: str) -> str:
        '''creating a session'''
        try:
            user = self._db.find_user_by(email=email)
            id = _generate_uuid()
            user.session_id = id
            return id
        except NoResultFound:
            pass

    def get_user_from_session_id(self, session_id: str) -> User:
        '''returns the corresponding User or None'''
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        '''destroys a session'''
        self._db.update_user(user_id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        '''generate a UUID and update the user’s
        reset_token database field'''
        try:
            user = self._db.find_user_by(email=email)
            us_uuid = _generate_uuid()
            user.reset_token = us_uuid
            return us_uuid
        except Exception:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        '''update_password'''
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            pass_hashed = _hash_password(password)
            user.hashed_password = pass_hashed
            user.reset_token = None
        except Exception:
            raise ValueError
