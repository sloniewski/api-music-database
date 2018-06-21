from flask import request, g
from app.serializer.decorator import apply_media_type
from app.auth.decorator import token_required

from . import band
from .models import Band


@band.route('/<int:id>', methods=['GET'])
@apply_media_type(request=request)
def get_band(id):
    band = Band.query.get_or_404(id)
    return {'name': band.name }

@band.route('/<string:slug>', methods=['PUT', 'DELETE', 'PATCH'])
@token_required(request=request)
def band_handler(slug):

    def put():
        pass

    def patch():
        pass

    def delete(req, slug):
        return '!'

    handlers = {
        'put': put,
        'patch': patch,
        'delete': delete,
    }  
    return handlers[request.method.lower()](req=request, slug=slug)


@band.route('/', methods=['GET'])
@apply_media_type(request=request)
def get_bands():
    data = {
        'records': 2,
        'next_page': 'page_url/?page=3',
        'prev_page': 'page_url/?page=1',
        'results': [
            {'name': 'Foo fighters' },
            {'name': 'Stereophonics' } ,
        ]
    }
    return data


@band.route('/', methods=['POST'])
@token_required(request=request)
def post_bands():
    return '!'
