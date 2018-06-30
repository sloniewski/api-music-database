import json
from collections import namedtuple
from functools import wraps

from flask import abort, Response, g

from app.main.serializer import Serializer


def make_response(function):
    @wraps(function)
    def decorator(*args, **kwargs):
        result = function(*args, **kwargs)
        response = Response()
        response.response = result[0]
        response.status_code = result[1]
        return response
    return decorator


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


class AcceptHeader(object):

    def __init__(self, mime_type, q):
        self.mime_type = mime_type
        self.q = q

    def __gt__(self, other):
        return self.q > other.q

    def __lt__(self, other):
        return self.q < other.q

    def __ge__(self,other):
        return self.q > other.q

    def __le__(self, other):
        return self.q < other.q

    def __eq__(self, other):
        return self.q == other.q

    def __ne__(self, other):
        return self.q != other.q

    def __str__(self):
        return "{} ; {}".format(self.mime_type, self.q)

    def __repr__(self):
        return self.__str__()

def parse_accept_headers(text):
    types_list = text.split(',')
    for x in range(len(types_list)):
        mime_type = types_list[x].split(';')[0].strip(' ')
        q = 1.0
        for arg in types_list[x].split(';')[1:]:
            key, value = arg.split('=')
            if key == 'q':
                q = float(value)
        types_list[x] = AcceptHeader(mime_type, q)
    return types_list


def negotiate_content_type(request, consumes):
    accept_header = request.headers.get('Accept')
    if accept_header is None:
        return 'application/json'

    mimi_type_objects = parse_accept_headers(accept_header)
    mimi_type_objects.sort(reverse=True)
    result = []
    for object in mimi_type_objects:
        if object.mime_type in Serializer.supported_types():
            result.append(object)
    return result[0].mime_type


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


