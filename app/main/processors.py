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


def process_response(function):
    @wraps(function)
    def decorator(*args, **kwargs):
        data = function(*args, **kwargs)
        resp = Response(response=data)
        try:
            resp.headers['Content-Type'] = g.content_type
        except AttributeError:
            resp.headers['Content-Type'] = 'text/plain'

        try:
            resp.status_code = g.status_code
        except AttributeError:
            resp.status_code = 200

        return resp
    return decorator
