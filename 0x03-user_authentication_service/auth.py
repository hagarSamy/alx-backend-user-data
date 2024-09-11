#!/usr/bin/env python3
"""
auth
"""

import bcrypt
from db import DB
from user import User


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
        