from flask import request

from app import db
from app.main.serializer import serialize_response
from app.main.processors import process_headers, make_response

from . import artist
from .models import Artist


@artist.route('/<int:id>', methods=['GET'])
@serialize_response
@process_headers(request)
@make_response
def get_artist(id):
    item = Artist.query.get_or_404(id)
    return item.as_dict(), 200
