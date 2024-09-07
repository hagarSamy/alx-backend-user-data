#!/usr/bin/env python3
'''auth module'''

from flask import request
from typing import List, TypeVar
import os


User = TypeVar('User')


class Auth:
    '''a class template for all authentication system'''
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        '''require_auth'''
        if path is not None:
            if path[-1] != '/':
                path += '/'
        if (
            path is None or
            excluded_paths is None or
            path not in excluded_paths
        ):
            return True
        return False

    def authorization_header(self, request=None) -> str:
        '''authorization_header'''
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> User:
        '''urrent_user'''
        return None

    def session_cookie(self, request=None):
        '''returns a cookie value from a request'''
        if request is None:
            return None
        session_name = os.getenv('SESSION_NAME', '_my_session_id')
        cookie_value = request.cookies.get(session_name)
        return cookie_value
