import json
from functools import wraps

from flask import abort, Response, g

from app.main.serializer import Serializer


def validate_request(req, expected_args, strict=True):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            serializer = Serializer(req)
            data = serializer.deserialize(req.data)

            errors = {'errors': []}
            if strict is True:
                missing = set(expected_args) - set(data)
                if len(missing) != 0:
                    errors['errors'].append(
                        'missing data in json: {}'.format(str(missing)[1:-1])
                    )

            extra = set(data) - set(expected_args)
            if len(extra) != 0:
                errors['errors'].append(
                    'got unexpected data: {}'.format(str(extra)[1:-1])
                )

            if len(errors['errors']) >= 1:
                abort(400, errors)

            return func(*args, **kwargs)
        return wrapper
    return decorator


def negotiate_content_type(request, consumes):
    return consumes[0]


def process_headers(request, consumes=['application/json']):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            response = function(*args, **kwargs)

            content_type = negotiate_content_type(request, consumes)
            response.headers['Content-Type'] = content_type
            g.content_type = content_type

            return response
        return wrapper
    return decorator


def make_response(function):
    @wraps(function)
    def decorator(*args, **kwargs):
        result = function(*args, **kwargs)
        response = Response()
        response.response = result[0]
        response.status_code = result[1]
        return response
    return decorator
