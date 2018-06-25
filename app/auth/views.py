from flask import abort, Response, request
from . import auth

from app import db

from .models import User, Token
from .functions import login_user
from .decorator import token_required


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
    response = Response(
        status=200,
        headers={'X-Auth-Token': token}
    )
    return response


@auth.route('/logout', methods=["POST"])
@token_required(request=request)
def destroy_token():
    '''destroys all tokens for user'''

    uuid = request.headers.get('X-Auth-Token')
    token = Token.query.filter(uuid == uuid).first()
    token_list = Token.query.filter(Token.user == token.user).all()
    for token in token_list:
        db.session.delete(token)
    db.session.commit()
    return '', 200
