from trumpbot.api import app
from trumpbot.sql import db
import json
import unittest
import base64
import os

unittest.TestLoader.sortTestMethodsUsing = None

with open('samples.json') as f:
    samples = json.load(f)


class APITest(unittest.TestCase):
    creds = {}

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

        db.init_app(app=app)
        db.create_all(app=app)

        self.app = app.test_client()

    def test_client(self):
        response = self.app.post(
            '/clients',
            data=json.dumps(samples['/clients']),
            headers={'Content-Type': 'application/json'}
        )

        data = json.loads(response.get_data(as_text=True))
        self.creds['client_id'] = data['client_id']
        self.creds['client_secret'] = data['client_secret']

        self.assertEqual(response.status_code, 201)

    def test_register(self):
        response = self.app.post(
            '/register',
            data=samples['/register'],
            headers={'Content-Type': 'multipart/form-data'}
        )

        self.assertEqual(response.status_code, 201)

    @unittest.skip("skipping oauth test")
    def test_oauth2_token(self):
        s = '{}:{}'.format(self.creds['client_id'], self.creds['client_secret'])
        s = str(base64.urlsafe_b64encode(s.encode('utf-8')), 'utf-8')

        response = self.app.post(
            '/oauth2/token',
            data=samples['/oauth2/token'],
            headers={
                'Authorization': 'Basic ' + s,
                'Content-Type': 'multipart/form-data'
            }
        )

        data = json.loads(response.get_data(as_text=True))
        del self.creds['client_id']
        del self.creds['client_secret']
        self.creds['access_token'] = data['access_token']

        self.assertEqual(response.status_code, 201)

    @classmethod
    def tearDownClass(cls):
        os.remove('../trumpbot/test.db')


if __name__ == '__main__':
    unittest.main()