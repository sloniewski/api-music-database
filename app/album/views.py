from flask import Blueprint

from app.decorators import auth

album = Blueprint('album', __name__)

@album.route('/1')
def test_1():
    auth.foo()
    return 'album'