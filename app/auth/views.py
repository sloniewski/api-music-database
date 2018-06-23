from . import auth

from .models import User


@auth.route('/login')
def get_token():
    return '!'


@auth.route('/logout')
def destroy_token():
    return '!'
