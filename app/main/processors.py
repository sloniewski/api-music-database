import json

def validate_request(req, expected_args, strict=True):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                data = req.get_json()
            except json.decoder.JSONDecodeError:
                abort(400, {'error': 'unable to parse json'})

            missing = set(expected_args) - set(data)
            errors = {'errors': []}
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
