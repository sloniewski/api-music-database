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

        self.test_band = Band(
            name='test1', city='abc', year_founded=1999, country='lebanon'
        )
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
            headers={'Accept': 'application/json'},
        )
        self.assertEqual(response.status_code, 200)

    def test_patch_band(self):
        response = self.client.patch(
            'http://localhost:5000/bands/' + str(self.test_band.band_id),
            data=json.dumps({'city': 'xyz'}),
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-Auth-Token': self.test_user.get_token(),
            })
        json_response = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response['name'], 'test1')
        self.assertEqual(json_response['year_founded'], 1999)
        self.assertEqual(json_response['year_disbanded'], None)
        self.assertEqual(json_response['city'], 'xyz')
        self.assertEqual(json_response['country'], 'lebanon')

    def test_fail_patch_band(self):
        response = self.client.patch(
            'http://localhost:5000/bands/' + str(self.test_band.band_id),
            data=json.dumps({'city': 'xyz', 'test': 'test'}),
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-Auth-Token': self.test_user.get_token(),
            })
        self.assertEqual(response.status_code, 400)

    def test_put_band_create(self):
        response = self.client.put(
            'http://localhost:5000/bands/99',
            data=json.dumps({'name': 'deftones', 'year_founded': 1996,
                             'city': 'somecity', 'year_disbanded': 2011,
                             'country': 'USA'}),
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-Auth-Token': self.test_user.get_token(),
            })
        self.assertEqual(response.status_code, 201)

    def test_put_band_update(self):
        response = self.client.put(
            'http://localhost:5000/bands/' + str(self.test_band.band_id),
            data=json.dumps({'name': 'deftones', 'year_founded': 1996,
                             'city': 'somecity', 'year_disbanded': 2011,
                             'country': 'USA'}),
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-Auth-Token': self.test_user.get_token(),
            })
        self.assertEqual(response.status_code, 200)

    def test_fail_put_band(self):
        response = self.client.put(
            'http://localhost:5000/bands/' + str(self.test_band.band_id),
            data=json.dumps({'name': 'deftones', 'year_founded': 1996,
                             'city': 'somecity', 'year_disbanded': 2011,
                             }),
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-Auth-Token': self.test_user.get_token(),
            })
        self.assertEqual(response.status_code, 400)

    def test_post_bands(self):
        response = self.client.post(
            'http://localhost:5000/bands/',
            data=json.dumps({'name': 'deftones', 'year_founded': 1996,
                             'city': 'somecity', 'year_disbanded': 2011,
                             'country': 'USA'}),
            headers={
                'Content-Type': 'application/json',
                'X-Auth-Token': self.test_user.get_token(),
            },
        )
        self.assertEqual(response.status_code, 201)

    def test_fail_post_bands(self):
        response = self.client.post(
            'http://localhost:5000/bands/',
            data=json.dumps({'year_founded': 1996, 'city': 'somecity',
                             'year_disbanded': 2011, 'country': 'USA'}),
            headers={
                'Content-Type': 'application/json',
                'X-Auth-Token': self.test_user.get_token(),
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_fail_post_bands_2(self):
        response = self.client.post(
            'http://localhost:5000/bands/',
            data=json.dumps({'name': 'deftones', 'year_founded': 1996,
                             'city': 'somecity', 'year_disbanded': 2011,
                            'country': 'USA', 'test': 'test'}),
            headers={
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'X-Auth-Token': self.test_user.get_token(),
            },
        )
        self.assertEqual(response.status_code, 400)


    def test_get_json_band(self):
        response = self.client.get(
            'http://localhost:5000/bands/{}'.format(self.test_band.band_id),
            headers={'Accept': 'application/json'},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers.get('Content-Type'), 'application/json')

    def test_get_xml_band(self):
        response = self.client.get(
            'http://localhost:5000/bands/{}'.format(self.test_band.band_id),
            headers={'Accept': 'application/xml'},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers.get('Content-Type'), 'application/xml')

    def test_delete_band(self):
        response = self.client.delete(
            'http://localhost:5000/bands/{}'.format(self.test_band_2.band_id),
            headers={'X-Auth-Token': self.test_user.get_token()},
        )
        self.assertEqual(response.status_code, 204)


if __name__ == '__main__':
    unittest.main()
