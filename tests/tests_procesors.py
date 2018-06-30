import unittest
from collections import namedtuple
from app.main.processors import  negotiate_content_type, parse_accept_headers, AcceptHeader


class TestProcessors(unittest.TestCase):

    def test_parse_accept_header(self):
        headers = parse_accept_headers(
            'application/xhtml+xml, application/xml;q=0.9, text/xml;q=0.7, text/html;q=0.5, text/plain;q=0.3'
        )
        for header in headers:
            self.assertIsInstance(header, AcceptHeader)

    def test_content_type_negotiation(self):
        Request = namedtuple('Request', ['headers'])
        mock_request= Request(
            headers={
                'Accept': 'application/xhtml+xml, application/xml;q=0.9, text/xml;q=0.7, text/html;q=0.5, text/plain;q=0.3'
            }
        )
        mime_type = negotiate_content_type(mock_request, consumes='application/xhtml+xml')
        self.assertEqual('application/xml', mime_type)
