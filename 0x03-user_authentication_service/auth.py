#!/usr/bin/env python3
"""
auth
"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    '''hashing pswd'''
    # Convert the password string to bytes
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password


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
            hashed_password = _hash_password(password)
            return bcrypt.checkpw(user.hashed_password, hashed_password)
        except:
            return False
