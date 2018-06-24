from flask import request, g, url_for

from app import db
from app.helpers import validate_json, PaginationHelper
from app.auth.decorator import token_required
from app.serializer.decorator import apply_media_type

from . import band
from .models import Band


@band.route('/<int:id>', methods=['GET'])
@apply_media_type(request=request)
def get_band(id):
    band = Band.query.get_or_404(id)
    return band.as_dict()


@band.route('/<int:id>', methods=['DELETE'])
@token_required(request=request)
def band_delete(id):
    band = Band.query.get_or_404(id)
    db.session.delete(band)
    return '', 204


@band.route('/<int:id>', methods=['PUT'])
@token_required(request=request)
def band_put(id):
    band = Band.query.get_or_404(id)
    return '!'


@band.route('/<int:id>', methods=['PATCH'])
@token_required(request=request)
def band_patch(id):
    band = Band.query.get_or_404(id)
    return '!'


@band.route('/', methods=['GET'])
@apply_media_type(request=request)
def get_bands():
    bands = db.session.query(Band)
    pagination = PaginationHelper(
        request=request,
        query=bands,
        items_per_page=3,
    )
    results = pagination.paginate(bands)
    resp = {
        "count": pagination.items_count,
        "next": None,
        "prev": None,
        'results': [x.as_dict() for x in results],
    }
    root = request.url_root[:-1]
    if pagination.next_page is not None:
        resp["next"] = root + url_for('.get_bands', page=pagination.next_page)
    if pagination.prev_page is not None:
        resp["prev"] = root + url_for('.get_bands', page=pagination.prev_page)
    return resp


@band.route('/', methods=['POST'])
@validate_json(request, 'name')
@token_required(request=request)
def post_bands():
    data = request.get_json()
    band = Band(name=data['name'])
    db.session.add(band)
    db.session.commit()
    return band.name, 201
