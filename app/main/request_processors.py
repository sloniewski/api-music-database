from functools import wraps

from flask import (
    abort,
    request,
    g,
)

from .serializer import Serializer


def process_request(func):
    @wraps(func)
    def decorator(*args, **kwargs):

        result = func(*args, **kwargs)

        # set response content type in global context
        accept_content_type = None
        def_q = 0
        for c_type, q in request.accept_mimetypes:
            if c_type in Serializer.supported_types() and q > def_q:
                accept_content_type = c_type
                def_q = q

        if accept_content_type == '*/*':
            accept_content_type = Serializer.default_type()

        if not accept_content_type:
            abort(415, 'requested media type is not supported')
        g.response_content_type = accept_content_type

        # check if request content type can be digested
        if request.method in ['POST', 'PUT', 'PATCH']:
            content_type = request.headers.get('Content-Type')
            if not content_type or content_type not in Serializer.accepted_types():
                abort(415, 'server did not recognize media type')

        return result
    return decorator


def validate_request_data(expected_args, strict=True):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            serializer = Serializer(request)
            data = serializer.deserialize(request.data)

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
