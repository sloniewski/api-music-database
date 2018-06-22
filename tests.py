import unittest
import os

from app import create_app, db


class TestBand(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        os.remove('app/test.db')        

    def testGetBands(self):
        response = self.client.get(
            'http://localhost:5000/bands/', 
            headers={'Content-Type': 'application/json'},
        )
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
