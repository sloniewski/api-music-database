from functools import wraps

from flask import abort, Response

from .base import Serializer


def apply_media_type(**kwargs):
    try:
        req = kwargs.pop('request')
    except KeyError:
        abort(500)

    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            content_type = req.headers.get('content_type')
            if content_type is None:
                content_type = 'application/json'
            if content_type.lower() not in Serializer.supported_types():
                content_type = 'application/json'

            data = Serializer.serialize(
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
