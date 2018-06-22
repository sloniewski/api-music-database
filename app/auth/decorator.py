
from flask import abort
from functools import wraps


def token_required(**kwargs):
    try:
        req = kwargs.pop('request')
    except KeyError:
        abort(500)
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            token = req.headers.get('X-Auth-Token')
            if token is None:
                abort(401)
            return function(*args, **kwargs)
        return wrapper
    return decorator
