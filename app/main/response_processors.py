from functools import wraps

from flask import (
    make_response,
    g,
)

from .serializer import Serializer


def process_response(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        result = func(*args, **kwargs)

        if g.response_content_type:
            serializer = Serializer(g.response_content_type)
            if isinstance(result, (tuple,)):
                data = serializer.serialize(result[0])
                result = tuple([data, *result[1:]])

        response = make_response(result)
        response.headers.add('Content-Language', 'en-US')
        response.headers.set('Content-Type', g.response_content_type)

        return response
    return decorator
