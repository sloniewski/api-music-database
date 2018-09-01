from flask import request

from app import db
from app.auth.decorator import token_required
from app.main.serializer import serialize_response
from app.main.processors import (
    process_headers,
    make_response,
)

from . import album
from .models import Album


@album.route('/<int:id>', methods=['GET'])
@serialize_response
@process_headers(request)
@make_response
def get_album(id):
    album = Album.query.get_or_404(id)
    return album.as_dict(), 200

@album.route('/', methods=['POST'])
@make_response
def post_album():
    data = request.get_json()
    album = Album(**data)
    db.session.add(album)
    db.session.commit()
    return 'album created', 201


@album.route('/<int:id>', methods=['DELETE'])
@make_response
def delete_album(id):
    album = Album.query.get_or_404
    db.session.delete(album)
    db.session.commit()
    return '', 204
    