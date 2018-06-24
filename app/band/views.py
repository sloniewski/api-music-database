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
    return '!'


@band.route('/<int:id>', methods=['PATCH'])
@token_required(request=request)
def band_patch(id):
    return '!'


@band.route('/', methods=['GET'])
@apply_media_type(request=request)
def get_bands():
    count_bands = db.session.query(Band).count()
    pagination = PaginationHelper(items_count=count_bands, items_per_page=3)

    page = pagination.validate_page(request.args.get('page'))
    if page is None:
        page = 1
    bands = db.session.query(Band).\
        offset(pagination.offset_for_page(page)).\
        limit(pagination.items_per_page)
    resp = {
        "count": count_bands,
        "next": url_for('.get_bands', page=(page+1)),
        "previous": url_for('.get_bands', page=(page-1)),
        'results': [x.as_dict() for x in bands],
    }
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
