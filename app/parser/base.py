import dicttoxml
import json


class Parser:
    parsers = {
        'application/json': json.dumps,
        'application/xml': dicttoxml.dicttoxml,
    }

    @classmethod
    def get_parser_for_type(cls, content_type):
        return cls.parsers[content_type]

    @classmethod
    def parse(cls, data_dict, content_type, **kwargs):
        parser = cls.get_parser_for_type(content_type)
        return parser(data_dict, **kwargs)

    @classmethod
    def supported_types(cls):
        return cls.parsers.keys()
