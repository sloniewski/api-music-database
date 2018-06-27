from . import album
from .models import Album

from app import db


@album.route('/<int:id>', methods=['GET'])
def get_album(id):
    album = Album.query.get_or_404(id)
    return album.name


@album,route('/<int:id>', methods=['DELETE'])
def delete_album(id):
    album = Album.query.get_or_404
    db.session.delete(album)
    db.session.commit()
    return '', 204
    