#!/usr/bin/env python3
"""
hashing password
"""

import bcrypt


def _hash_password(password: str) -> bytes:
    '''hashing pswd'''
    # Convert the password string to bytes
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password
