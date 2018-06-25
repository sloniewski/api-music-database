import json
from functools import wraps

from flask import abort, Response
import dicttoxml


import dicttoxml
import json

from flask import abort

    
class JsonSerializer:
    
    def serialize(self, data):
        try:
            data = json.dumps(data)
        except Exception:
            abort(415)
        return data

class XmlSerializer:
    
    def serialize(self, data):
        try:
            data = dicttoxml.dicttoxml(data)
        except Exception:
            abort(415)
        return data

    
class Serializer:
    serializer_class = {
        'application/json': JsonSerializer,
        'application/xml': XmlSerializer,
    }
    
    def __init__(self, content_type):
        try:
            self.serializer = self.serializer_class[content_type]
        except KeyError:
            self.serializer = JsonSerializer
    
    def serialize(self, data):
        return self.serializer.serialize(data)


def apply_media_type(**kwargs):
    try:
        req = kwargs.pop('request')
    except KeyError:
        abort(500)

    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            content_type = req.headers.get('content_type')
            serialzer = Serializer(content_type)
            response = function(*args, **kwargs)
            data = serializer.serialize(
                data=response.data,
                content_type=content_type,
            )
            response.headers.add('Content-Type': serializer.content_type)
            return response
        return wrapper
    return decorator
