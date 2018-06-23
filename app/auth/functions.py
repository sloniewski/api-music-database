from datetime import datetime
from .models import User, Token


def login_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user is not None and user.verify_password(password):
        return user
    return None


def validate_token(uuid):
    token = Token.query.filter(
        Token.uuid==uuid,
        Token.valid_to >= datetime.now()).first()
    if token is None:
        return False
    return True
