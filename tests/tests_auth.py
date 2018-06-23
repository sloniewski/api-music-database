import unittest

from app import create_app, db


class TestAuthModule(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

    def testLoginView(self):
        response = self.client.get(
            'http://localhost:5000/auth/login'
        )
        self.assertEqual(response.status_code, 200)

    def testLogoutView(self):
        response = self.client.get(
            'http://localhost:5000/auth/login'
        )
        self.assertEqual(response.status_code, 200)
