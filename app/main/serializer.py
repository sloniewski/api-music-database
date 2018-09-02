import json
import xml.etree.ElementTree as ET
from functools import wraps

import dicttoxml
from flask import abort, g


class BaseSerializer:

    def serialize(self, data):
        raise NotImplementedError('method not implemented')

    def deserialize(self, data):
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
            print(error.msg)
            abort(415, error.msg)
        return data


class TextSerializer(BaseSerializer):

    def serialize(self, data):
        return str(data)

    def deserialize(self, data):
        return data


class XmlSerializer(BaseSerializer):

    def serialize(self, data):

        if isinstance(data, (str, int)):
            data = [data]

        try:
            data = dicttoxml.dicttoxml(data)
        except Exception as err:
            abort(415, str(err))
        return data

    def deserialize(self, data):
        xml = ET.fromstring(data)
        return xml


class Serializer:
    _default_type = 'application/json'

    serializer_class = {
        '*/*': JsonSerializer,
        'application/json': JsonSerializer,
        'application/xml': XmlSerializer,
        'text/html': TextSerializer,
        'text/plain': TextSerializer,
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

    @classmethod
    def supported_types(cls):
        return cls.serializer_class.keys()

    @staticmethod
    def accepted_types():
        return ['application/json', 'application/xml']

    @classmethod
    def default_type(cls):
        return cls._default_type

    def serialize(self, data):
        return self.serializer.serialize(data)

    def deserialize(self, data):
        return self.serializer.deserialize(data)


def serialize_response(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        response = func(*args, **kwargs)

        serializer = Serializer(g.content_type)
        data = serializer.serialize(response.response)
        response.response = data

        return response
    return decorator
