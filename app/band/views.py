from flask import request, url_for, Response

from app import db
from app.auth.decorator import token_required
from app.main.serializer import apply_media_type, Serializer
from app.main.pagination import PaginationHelper
from app.main.processors import validate_request, process_response

from . import band
from .models import Band


@band.route('/<int:id>', methods=['GET'])
@process_response
@apply_media_type(request)
def get_band(id):
    band = Band.query.get_or_404(id)
    return band.as_dict()


@band.route('/<int:id>', methods=['DELETE'])
@token_required(request)
def band_delete(id):
    band = Band.query.get_or_404(id)
    db.session.delete(band)
    return '', 204


@band.route('/<int:id>', methods=['PUT'])
@process_response
@apply_media_type(request)
@validate_request(request, ['name', 'year_founded', 'city', 'year_disbanded', 'country'])
@token_required(request)
def band_put(id):
    band = Band.query.get_or_404(id)
    raise NotImplementedError('not implemented !!')
    # 200 OK or 201 created, or 409 Conflict
    return '!'


@band.route('/<int:id>', methods=['PATCH'])
@process_response
@apply_media_type(request)
@validate_request(request, ['name', 'year_founded', 'city', 'year_disbanded', 'country'], strict=False)
@token_required(request)
def band_patch(id):
    band = Band.query.get_or_404(id)

    content_type = request.headers.get('Content-Type')
    serializer = Serializer(content_type)
    data = serializer.deserialize(request.data)

    for key, value in data.items():
        setattr(band, key, value)

    db.session.add(band)
    db.session.commit()

    return band.as_dict()


@band.route('/', methods=['GET'])
@process_response
@apply_media_type(request)
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
@validate_request(request, ['name', 'year_founded', 'city', 'year_disbanded', 'country'])
@token_required(request)
def post_bands():
    data = request.get_json()
    band = Band(name=data['name'])
    db.session.add(band)
    db.session.commit()
    return band.name, 201
