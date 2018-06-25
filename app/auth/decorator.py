from flask import abort
from functools import wraps

from .functions import validate_token


def token_required(req):

    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            token = req.headers.get('X-Auth-Token')
            if not validate_token(token):
                abort(401, {'errors': 'invalid or expired token'})
            return function(*args, **kwargs)
        return wrapper
    return decorator
