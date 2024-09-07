#!/usr/bin/env python3
'''auth module'''

from flask import request
from typing import List, TypeVar

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
