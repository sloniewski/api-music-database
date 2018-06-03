from flask import Blueprint


album = Blueprint('album', __name__)

@album.route('/1')
def test_1():
    return 'album'