#!/usr/bin/env python3
'''auth module'''

from flask import request
from typing import List, TypeVar

User = TypeVar('User')


class Auth:
    '''a class template for all authentication system'''
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''require_auth'''
        return False

    def authorization_header(self, request=None) -> str:
        '''authorization_header'''
        return None

    def current_user(self, request=None) -> User:
        '''urrent_user'''
        return None
