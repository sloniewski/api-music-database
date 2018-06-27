import unittest

from werkzeug.exceptions import UnsupportedMediaType

from app.main.serializer import XmlSerializer, JsonSerializer


class TestSerializers(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def test_dict_to_xml(self):
        serializer = XmlSerializer()
        data = {'a': 1, 'b': 'abc', 'c': [1, 2, 'x']}
        result = serializer.serialize(data)
        self.assertIsInstance(result, str)
                
    def test_xml_to_dict(self):
        serializer = XmlSerializer()
        data = '''<?xml version="1.0" encoding="UTF-8"?>
                    <note>
                      <to>Tove</to>
                      <from>Jani</from>
                      <heading>Reminder</heading>
                      <body>Don't forget me this weekend!</body>
                    </note>'''
        result = serializer.deserialize(data)
        self.assertIsInstance(result, dict)
        self.assertEqual(['a','b','c'], result.keys())
    
    def test_fail_dict_to_xml(self):
        serializer = XmlSerializer()
        data = {'a': 1, 'b': 'abc', 'c': [1, 2, 'x']}
        with self.assertRaises(UnsupportedMediaType):
            result = serializer.serialize(data)
    
    def test_fail_xml_to_dict(self):
        serializer = XmlSerializer()
        data = '''<?xml version="1.0" encoding="UTF-8"?>
                <note>
                  <to>Tove</to>
                  <from>Jani</from>
                  <heading>Reminder</heading>
                  <body>Don't forget me this weekend!</body>
                </note>'''
        with self.assertRaises(UnsupportedMediaType):
            result = serializer.deserialize(data)
           
    def test_dict_to_json(self):
        serializer = JsonSerializer()
        data = {'a': 1, 'b': 'abc', 'c': [1, 2, 'x']}
        result = serializer.serialize(data)
        self.assertIsInstance(result, str)
    
    def test_json_to_dict(self):
        serializer = JsonSerializer()
        data = '{"name":"John", "age":30, "car":null}' #json
        result = serializer.deserialize(data)
        self.assertIsInstance(result, dict)
        self.assertEqual(['a','b','c'], result.keys())
    
    def test_fail_dict_to_json(self):
        serializer = JsonSerializer()
        data = {'a': 1, 'b': 'abc', 'c': [1, 2, 'x']}
        with self.assertRaises(UnsupportedMediaType):
            result = serializer.serialize(data)
        
    def test_fail_json_to_dict(self):
        serializer = JsonSerializer()
        data = '{"name":"John", "age":30, "car":null}' #json
        with self.assertRaises(UnsupportedMediaType):
            result = serializer.deserialize(data)
           