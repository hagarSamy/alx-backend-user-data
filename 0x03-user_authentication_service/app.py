#!/usr/bin/env python3
""" Flask Application """

from flask import Flask, jsonify, request, abort, make_response, redirect
from auth import Auth

AUTH = Auth()


app = Flask(__name__)


@app.route('/', methods=['GET'])
def root():
    """ home route """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users():
    '''register'''
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    '''login'''
    email = request.form.get('email')
    password = request.form.get('password')
    if not AUTH.valid_login(email, password):
        abort(401)
    else:
        session_id = AUTH.create_session(email)
        response = make_response(
            jsonify({"email": email, "message": "logged in"}), 200
        )
        response.set_cookie("session_id", session_id)
        return response


@app.route('/sessions', methods=['DELETE'])
def logout():
    '''logout'''
    session_id = request.cookies.get('session_id')
    try:
        user = AUTH.get_user_from_session_id(session_id)
        AUTH.destroy_session(user.id)
        return redirect('/')
    except Exception:
        abort(403)


@app.route('/profile', methods=['GET'])
def profile():
    '''logout'''
    session_id = request.cookies.get('session_id')
    try:
        user = AUTH.get_user_from_session_id(session_id)
        return jsonify({"email": user.email}), 200
    except Exception:
        abort(403)


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    '''get_reset_password_token'''
    email = request.form.get('email')
    try:
        user = AUTH._db.find_user_by(email=email)
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token}), 200
    except Exception:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
