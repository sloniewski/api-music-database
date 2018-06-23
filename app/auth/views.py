from flask import abort, Response
from . import auth

from .models import User
from . import login_user


@auth.route('/login', methods=["POST"])
def get_token():
    try:
        username = request.authorization['username']
        password = request.authorization['password']
    except (TypeError, KeyError, AttributeError):
        abort(400)
    user = login_user(username, password)
    if user is None:
        abort(401)
    token = user.get_token()
    
    return '!'


@auth.route('/logout', methods=["POST"])
def destroy_token():
    return '!'
