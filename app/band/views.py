from flask import request, g
from app.serializer.decorator import apply_media_type
from app.auth.decorator import token_required

from . import band


@band.route('/<string:slug>', methods=['GET'])
@apply_media_type(request=request)
def get_band(slug):
    data = {
        'uid': slug,
        'name': 'Foo Fighters',
        'date': '1995',
    }
    return data

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
