from . import album


@album.route('/1')
def test_1():
    return 'album'
