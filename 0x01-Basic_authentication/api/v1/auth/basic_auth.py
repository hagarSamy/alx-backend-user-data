#!/usr/bin/env python3
'''BasicAuth module'''

from api.v1.auth.auth import Auth
from base64 import b64decode, binascii
import re
from typing import Union, TypeVar


class BasicAuth(Auth):
    '''handling BasicAuth'''
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        '''returns the Base64 part of
        the Authorization header for a Basic Authentication'''
        if (
            authorization_header is None or
            type(authorization_header) is not str or
            not authorization_header.startswith('Basic ')
        ):
            return None
        return authorization_header[len('Basic '):]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                               str) -> str:
        '''returns the decoded value of
        a Base64 string base64_authorization_header'''
        if (
            base64_authorization_header is None or
            type(base64_authorization_header) is not str
        ):
            return None
        base64_pattern = re.compile(r'^[A-Za-z0-9+/]*={0,2}$')
        if not base64_pattern.match(base64_authorization_header):
            return None
        try:
            return b64decode(base64_authorization_header).decode('utf-8')
        except (binascii.Error, UnicodeDecodeError):
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> Union[str, str]:
        '''returns the user email and password from the Base64 decoded value'''
        if (
            decoded_base64_authorization_header is None or
            type(decoded_base64_authorization_header) is not str or
            ':' not in decoded_base64_authorization_header
        ):
            return None, None
        return tuple(decoded_base64_authorization_header.split(':', 1))

    def user_object_from_credentials(self, user_email:
                                     str, user_pwd: str) -> TypeVar('User'):
        '''returns the User instance based on his email and password.'''
        if (
            user_email is None or
            type(user_email) is not str or
            user_pwd is None or
            type(user_pwd) is not str
        ):
            return None
        try:
            user = User.search({"email": user_email})
        except Exception:
            return None

        if not user:
            return None
        if user.is_valid_password(user_pwd):
            return user
