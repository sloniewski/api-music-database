from . import album
from .models import Album

@album.route('/<int:id>')
def get_album(id):
    album = Album.query.get_or_404(id)
    return album.name
