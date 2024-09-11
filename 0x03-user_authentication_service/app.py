#!/usr/bin/env python3
""" Flask Application """

from flask import Flask, jsonify, request, abort, make_response
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
