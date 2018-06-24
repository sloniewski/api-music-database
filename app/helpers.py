import json
from functools import wraps

from flask import abort


class PaginationHelper:
    page_arg = 'page'

    def __init__(self, request, query, items_per_page=10):
        page_input = self.validate_page(request.args.get(self.page_arg))
        if page_input is not None:
            self.page = page_input
        else:
            self.page = 1
        self.items_count = query.count()
        self.items_per_page = items_per_page

    @property
    def page_count(self):
        if self.items_count % self.items_per_page == 0:
            page_count = self.items_count / self.items_per_page
        else:
            page_count = (self.items_count // self.items_per_page) + 1
        return page_count

    @property
    def offset(self):
        return self.offset_for_page()

    @property
    def next_page(self):
        if self.page + 1 > self.page_count:
            return None
        return self.page + 1

    @property
    def prev_page(self):
        if self.page - 1 <= 0:
            return None
        return self.page - 1

    def offset_for_page(self):
        if self.page <= 1:
            return 0
        if self.page > self.page_count:
            return self.items_per_page * (self.page_count - 1)
        return self.items_per_page * (self.page - 1)

    @staticmethod
    def validate_page(page):
        if page is None:
            return None
        if isinstance(page, (str)) and not page.isdigit():
            return None
        try:
            page = int(page)
        except ValueError:
            return None
        return page

    def paginate(self, query):
        return query.\
            offset(self.offset).\
            limit(self.items_per_page)


def validate_json(req, *expected_args):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                data = req.get_json()
            except json.decoder.JSONDecodeError:
                abort(400, {'error': 'unable to parse json'})

            missing = set(expected_args) - set(data)
            if len(missing) != 0:
                abort(
                    400, {'error': 'missing data in json: {}'.format(str(missing)[1:-1])})

            extra = set(data) - set(expected_args)
            if len(extra) != 0:
                abort(
                    400, {'error': 'got unexpected data: {}'.format(str(extra)[1:-1])})

            return func(*args, **kwargs)
        return wrapper
    return decorator


def jsonify_response(code):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            data = func(*args, **kwargs)
            return Response(
                status=code,
                response=json.dumps(data, indent=4),
                headers=[('Content-Type', 'application/json')]
            )
        return wrapper
    return decorator
