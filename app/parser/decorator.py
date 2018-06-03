from functools import wraps

from flask import abort, Response

from .base import Parser

def apply_media_type(req):
    content_type = req.headers.get('content_type')
    if content_type.lower() not in Parser.supported_types():
        abort(415)
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            data = Parser.parse(
                data_dict=function(*args, **kwargs),
                content_type=content_type
            )
            headers = {
                'Content-Type': content_type,
            }
            return Response(
                response=data,
                headers=headers,
            )
        return wrapper
    return decorator