#!/usr/bin/env python3
""" Module of session views
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def release_session() -> str:
    """ POST /auth_session/login
    Return:
      - starts a new session
    """
    email = request.form.get('email')
    pswd = request.form.get('password')
    if email is None:
        return jsonify({"error": "email missing"}), 400
    if pswd is None:
        return jsonify({"error": "password missing"}), 400
    users = User.search({"email": email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 401
    for user in users:
        if user.is_valid_password(pswd):
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            jsoned_user = jsonify(user.to_json())
            session_name = os.getenv('SESSION_NAME')
            jsoned_user.set_cookie(session_name, session_id)
            return jsoned_user
    return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout',
                 methods=['DELETE'], strict_slashes=False)
def handle_logout():
    """
    Handle user logout
    """
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
