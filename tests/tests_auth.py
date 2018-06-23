import unittest
import base64

from app import create_app, db
from app.auth.models import User


from unittest import skip

class TestAuthModule(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()
        self.test_user = User(username='abc')
        self.test_user.set_password('abc')
        db.session.add(self.test_user)
        db.session.commit()

    def tearDown(self):
        db.drop_all()

    def test_password_setter(self):
        user_1 = User(username='user_1')
        user_2 = User(username='user_2')
        user_1.set_password('abc')
        user_2.set_password('abc')
        self.assertNotEqual(user_1._password_hash, user_2._password_hash)

    def test_password_verification(self):
        self.assertTrue(self.test_user.verify_password('abc'))
        self.assertFalse(self.test_user.verify_password('xyz'))

    def test_login_view(self):
        response = self.client.post(
            'http://localhost:5000/auth/login'
        )
        self.assertEqual(response.status_code, 400)

    def test_fail_login(self):
        auth_string = base64.b64encode(b'abc:xyz').decode('utf-8')
        response = self.client.post(
            'http://localhost:5000/auth/login',
            headers=({
                'Authorization': 'Basic ' + auth_string,
            }),
        )
        self.assertEqual(response.status_code, 401)

    def test_login_succes(self):
        auth_string = base64.b64encode(b'abc:abc').decode('utf-8')
        response = self.client.post(
            'http://localhost:5000/auth/login',
            headers=({
                'Authorization': 'Basic ' + auth_string,
            }),
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.headers.get('X-Auth-Token'))

    def test_logout_view(self):
        response = self.client.post(
            'http://localhost:5000/auth/login'
        )
        self.assertEqual(response.status_code, 200)
