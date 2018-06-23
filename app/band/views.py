from flask import request, g
from app.serializer.decorator import apply_media_type
from app.auth.decorator import token_required
from app import db


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
def band_put(slug):
    return '!'


@band.route('/<int:id>', methods=['PATCH'])
@token_required(request=request)
def band_patch(slug):
    return '!'



@band.route('/', methods=['GET'])
@apply_media_type(request=request)
def get_bands():
    return '!'


@band.route('/', methods=['POST'])
@token_required(request=request)
def post_bands():
    return '!'
