from flask import Blueprint

band = Blueprint('band', __name__)

@band.route('/band')
def test_2():
    return 'band'