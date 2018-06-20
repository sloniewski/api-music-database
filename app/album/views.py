from . import album
from .models import Album

@album.route('/<pk>')
def test_1(pk):
    album = Album.query.get_or_404(pk)
    return album.name
