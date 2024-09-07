#!/usr/bin/env python3
'''session_auth module'''

from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    '''session auth class that will create a new auth mechanism to
    - validate if everything inherits correctly without any overloading
    - validate the “switch” by using environment variables'''
    pass
