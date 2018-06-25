import json
from functools import wraps

from flask import abort, Response
import dicttoxml


class Serializer:
    serializers = {
        'application/json': json.dumps,
        'application/xml': dicttoxml.dicttoxml,
    }

    @classmethod
    def get_serializer_for_type(cls, content_type):
        return cls.serializers[content_type]

    @classmethod
    def serialize(cls, data_dict, content_type, **kwargs):
        serializer = cls.get_serializer_for_type(content_type)
        return serializer(data_dict, **kwargs)

    @classmethod
    def supported_types(cls):
        return cls.serializers.keys()


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
