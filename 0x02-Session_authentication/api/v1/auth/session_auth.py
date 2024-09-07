#!/usr/bin/env python3
'''session_auth module'''

from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    '''session auth class that will create a new auth mechanism to
    - validate if everything inherits correctly without any overloading
    - validate the “switch” by using environment variables'''
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        '''creates a Session ID for a user_id'''
        if(
            user_id is None or
            type(user_id) is not str
        ):
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        ''' returns a User ID based on a Session ID'''
        if(
            session_id is None or
            type(session_id) is not str
        ):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        '''returns a User instance based on a cookie value'''
        session_id  = self.session_cookie(request)
        if not session_id:
            return None
        user_id = self.user_id_for_session_id(session_id)
        user = User.get(user_id)
