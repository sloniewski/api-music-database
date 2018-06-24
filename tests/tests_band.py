import json
import os
import unittest

from app import create_app, db

from app.band.models import Band
from app.auth.models import User


class TestBandCollection(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()
        self.test_band = Band(name='test1')
        self.test_band_2 = Band(name='test2')
        self.test_user = User(username='abc')
        self.test_user.set_password('abc')
        db.session.add(self.test_user)
        db.session.add(self.test_band_2)
        db.session.add(self.test_band)
        db.session.commit()

    def tearDown(self):
        db.drop_all()

    def test_get_bands(self):
        response = self.client.get(
            'http://localhost:5000/bands/',
            headers={'Content-Type': 'application/json'},
        )
        self.assertEqual(response.status_code, 200)

    def test_post_bands(self):
        response = self.client.post(
            'http://localhost:5000/bands/',
            data=json.dumps({'name': 'deftones'}),
            headers={
                'Content-Type': 'application/json',
                'X-Auth-Token': self.test_user.get_token(),
            },
        )
        self.assertEqual(response.status_code, 201)

    def test_get_band(self):
        response = self.client.get(
            'http://localhost:5000/bands/{}'.format(self.test_band.band_id),
            headers={'Content-Type': 'application/json'},
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_band(self):
        response = self.client.delete(
            'http://localhost:5000/bands/{}'.format(self.test_band_2.band_id),
            headers={'X-Auth-Token': self.test_user.get_token()},
        )
        self.assertEqual(response.status_code, 204)


if __name__ == '__main__':
    unittest.main()
