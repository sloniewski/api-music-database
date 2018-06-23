from flask import abort, Response, request
from . import auth

from .models import User
from .functions import login_user


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
    token = '123456' #user.get_token()

    response = Response(
        status=200,
        headers={'X-Auth-Token':token}
    )
    return response


@auth.route('/logout', methods=["POST"])
def destroy_token():
    return '!'
