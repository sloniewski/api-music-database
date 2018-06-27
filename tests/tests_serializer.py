import unittest

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
        data = '{"name":"John", "age":30, "car":null}' #json
        result = serializer.deserialize(data)
        self.assertIsInstance(result, dict)
        self.assertEqual(['a','b','c'], result.keys())
    
    def test_fail_dict_to_xml(self):
        pass
    
    def test_fail_xml_to_dict(self):
        pass
    
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
    
    def test_fail_dict_to_xml(self):
        pass
    
    def test_fail_xml_to_dict(self):
        pass