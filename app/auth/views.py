from flask import abort, Response, request
from . import auth

from app import db
from app.main.request_processors import (
    validate_request_data,
    process_request,
    Serializer,
)
from app.main.response_processors import (
    process_response,
)

from .models import User, Token
from .functions import login_user
from .decorator import token_required


@auth.route('/login', methods=['GET', "POST"])
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
@token_required(request)
def destroy_token():
    """destroys all tokens for user"""

    uuid = request.headers.get('X-Auth-Token')
    token = Token.query.filter(uuid == uuid).first()
    token_list = Token.query.filter(Token.user == token.user).all()
    for token in token_list:
        db.session.delete(token)
    db.session.commit()
    return '', 200


@auth.route('/users', methods=['POST'])
@process_response
@validate_request_data(['username', 'password'])
@process_request
@token_required(request)
def create_user():
    content_type = request.headers.get('Content-Type')
    serializer = Serializer(content_type)
    data = serializer.deserialize(request.data)
    user = User(username=data['username'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return 'user created', 201


@auth.route('/users/<int:id>', methods=['GET'])
@process_response
@process_request
@token_required(request)
def get_user(id):
    user = User.query.get_or_404(id)
    return user.as_dict(), 200
