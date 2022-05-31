#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import firebase_admin
from firebase_admin import auth
import json

from flask import Flask, abort, request, session, jsonify, render_template, redirect

app = Flask(__name__)
app.secret_key = 'super secret key'
app.debug = True

default_app = firebase_admin.initialize_app()
print default_app.name

@app.route('/')
def index():
    print default_app
    return render_template("index.html")

@app.route('/sessionLogin', methods=['POST'])
def session_login():
    # Get the ID token sent by the client
    id_token = request.json['idToken']
    # Set session expiration to 5 days.
    expires_in = datetime.timedelta(days=5)
    try:
        # Create the session cookie. This will also verify the ID token in the process.
        # The session cookie will have the same claims as the ID token.
        session_cookie = auth.create_session_cookie(id_token, expires_in=expires_in)
        response = jsonify({'status': 'success'})
        # Set cookie policy for session cookie.
        expires = datetime.datetime.now() + expires_in
        response.set_cookie('session', session_cookie, expires=expires, httponly=True, secure=True)
        return response
    except Exception as e:
        print e
        return abort(401, 'Failed to create a session cookie')

@app.route('/secret', methods=['GET'])
def access_restricted_content():
    session_cookie = request.cookies.get('session')
    if not session_cookie:
        # Session cookie is unavailable. Force user to login.
        return redirect('/')

    # Verify the session cookie. In this case an additional check is added to detect
    # if the user's Firebase session was revoked, user deleted/disabled, etc.
    try:
        decoded_claims = auth.verify_session_cookie(session_cookie, check_revoked=True)
        print decoded_claims
        return render_template("secret.html")
    except auth.InvalidSessionCookieError:
        # Session cookie is invalid, expired or revoked. Force user to login.
        return flask.redirect('/')
