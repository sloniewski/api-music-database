from flask import Blueprint

from werkzeug.security import check_password_hash

auth = Blueprint('auth', __name__)

from . import views
from .models import User


def login_user(username, password):
    user = User.query.filter_by(username=username).first()
    if len(user) == 1 and user.verify_password(password):
        return user
    return None
