from flask import Blueprint, request
from app.parser.decorator import apply_media_type

band = Blueprint('band', __name__)


@band.route('/<string:slug>', methods=['GET', 'PUT', 'DELETE', 'PATCH'])
def band_handler(slug):

    @apply_media_type(request)
    def get(req, slug):
        data = {
            'uid': slug,
            'name': 'Foo Fighters',
            'date': '1995',
        }
        return data

    def delete(request, uid):
        return '!'

    handlers = {
        'get': get,
        'delete': delete,
    }
    return handlers[request.method.lower()](req=request, slug=slug)


@band.route('/', methods=['GET', 'POST'])
def bands_handlers():
    return 'band'


