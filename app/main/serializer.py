import dicttoxml
import json
from functools import wraps

from flask import abort, g

class BaseSerializer:

    def serialize(self, data):
        raise NotImplementedError('method not implemented')

    def deserialize(self,data):
        raise NotImplementedError('method not implemented')


class JsonSerializer(BaseSerializer):

    def serialize(self, data):
        try:
            data = json.dumps(data)
        except json.JSONDecodeError as error:
            abort(415, error.msg)
        return data

    def deserialize(self, data):
        try:
            data = json.loads(str(data, encoding='utf-8'))
        except json.JSONDecodeError as error:
            abort(415, error.msg)
        return data


class XmlSerializer(BaseSerializer):

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

    def get_serializer_class(self, content_type):
        return self.serializer_class[content_type]
    
    def __init__(self, content_type):
        try:
            self.serializer = self.get_serializer_class(content_type)()
            self.content_type = content_type
        except KeyError:
            self.serializer = JsonSerializer()
            self.content_type = 'application/json'

    def serialize(self, data):
        return self.serializer.serialize(data)

    def deserialize(self, data):
        return self.serializer.deserialize(data)


def apply_media_type(req):

    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            content_type = req.headers.get('Content-Type')
            serializer = Serializer(content_type)
            data = function(*args, **kwargs)
            data = serializer.serialize(data)
            g.content_type = serializer.content_type
            return data
        return wrapper
    return decorator
