import dicttoxml
import json


class Serializer:
    serializers = {
        'application/json': json.dumps,
        'application/xml': dicttoxml.dicttoxml,
    }

    @classmethod
    def get_serializer_for_type(cls, content_type):
        return cls.serializers[content_type]

    @classmethod
    def serialize(cls, data_dict, content_type, **kwargs):
        serializer = cls.get_serializer_for_type(content_type)
        return serializer(data_dict, **kwargs)

    @classmethod
    def supported_types(cls):
        return cls.serializers.keys()
