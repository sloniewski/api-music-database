from flask import request, url_for, Response, g

from app import db
from app.auth.decorator import token_required
from app.main.serializer import Serializer, serialize_response
from app.main.pagination import PaginationHelper
from app.main.processors import validate_request, process_headers

from app.main.response_processors import process_response
from app.main.request_processors import process_request, validate_request_data

from . import band
from .models import Band


@band.route('/<int:id>', methods=['GET'])
@process_response
@process_request
def get_band(id):
    band = Band.query.get_or_404(id)
    return band.as_dict(), 200


@band.route('/<int:id>', methods=['DELETE'])
@process_response
@token_required(request)
def band_delete(id):
    band = Band.query.get_or_404(id)
    db.session.delete(band)
    db.session.commit()
    return 'no content', 204


@band.route('/<int:id>', methods=['PUT'])
@process_response
@validate_request_data(['name', 'year_founded', 'city', 'year_disbanded', 'country'])
@process_request
@token_required(request)
def band_put(id):
    band = Band.query.filter(Band.band_id == id).first()
    serializer = Serializer(request)
    data = serializer.deserialize(request.data)
    if band is not None:
        band.set_attrs(**data)
        g.status_code = 200
    else:
        band = Band(band_id=id, **data)
        g.status_code = 201
    db.session.add(band)
    db.session.commit()
    return band.as_dict(), g.status_code


@band.route('/<int:id>', methods=['PATCH'])
@process_response
@validate_request_data(['name', 'year_founded', 'city', 'year_disbanded', 'country'], strict=False)
@process_request
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

    return band.as_dict(), 200


@band.route('/', methods=['GET'])
@process_response
@process_request
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
    return resp, 200


@band.route('/', methods=['POST'])
@process_response
@validate_request_data(['name', 'year_founded', 'city', 'year_disbanded', 'country'])
@process_request
@token_required(request)
def post_bands():
    serializer = Serializer(request.content_type)
    data = serializer.deserialize(request.data)
    band = Band(**data)
    db.session.add(band)
    db.session.commit()
    return band.as_dict(), 201
