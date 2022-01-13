import unittest

from flask_mongoengine import MongoEngine

from api.user.controllers import create_user
from api.models import user
from app import create_app
import flask
import json


class UserTestSuite(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')

        user.User.drop_collection()

        self.valid_user_data = {
            "first_name": "Test",
            "last_name": "McTest",
            "email": "test@testuser.io",
            "password": "supersecret"
        }

        self.invalid_user_data = {
            "first_name": "Test",
            "last_name": "McTest",
            "password": "supersecret"
        }

        self.valid_login_data = {
            "email": "test@testuser.io",
            "password": "supersecret"
        }

        self.invalid_login_data_password_bad = {
            "email": "test@testuser.io",
            "password": "supersecret1"
        }

        self.invalid_login_data_missing_user = {
            "email": "test_user_doesnt_exist@testuser.io",
            "password": "supersecret1"
        }

        return

    def test_create_user_success(self):
        with self.app.app_context():
            with self.app.test_request_context():
                response = create_user(self.valid_user_data)

                # jsonify
                (data, status) = response
                self.assertEqual(status, 201)

    def test_get_user_endpoint(self):
        with self.app.test_client() as c:
            new_user = user.User().save()
            response = c.get(f'/api/users/{new_user.id}')
            status = response.status
            data = json.loads(response.data.decode('utf-8'))

            self.assertEqual(status, '200 OK')
            self.assertIsNotNone(data)

    def test_create_user_endpoint_valid_data(self):
        with self.app.test_client() as c:
            response = c.post('/api/users', data=self.valid_user_data)
            status = response.status
            data = response.data.decode('utf-8')
            data = json.loads(data)

            self.assertEqual(status, '201 CREATED')
            self.assertIsNotNone(data)

    def test_create_user_endpoint_invalid_data(self):
        with self.app.test_client() as c:
            response = c.post('/api/users', data=self.invalid_user_data)
            status = response.status
            data = response.data.decode('utf-8')
            data = json.loads(data)

            self.assertEqual(status, '400 BAD REQUEST')

    def test_create_user_fail_duplicate_email(self):
        with self.app.test_client() as c:
            new_user = user.User(**self.valid_user_data)
            new_user.save()
            response = c.post('/api/users', data=self.valid_user_data)
            status = response.status
            data = response.data.decode('utf-8')
            data = json.loads(data)

            self.assertEqual(status, '400 BAD REQUEST')
            self.assertEqual(
                data['error'], 'user associated with this email (test@testuser.io) already exists')

    def test_user_login_successful(self):
        with self.app.app_context():
            with self.app.test_request_context():
                with self.app.test_client() as c:
                    new_user = c.post('/api/users', data=self.valid_user_data)

                    response = c.post('/api/users/login',
                                      data=self.valid_login_data)
                    status = response.status
                    data = response.data.decode('utf-8')
                    data = json.loads(data)
                    self.assertEqual(status, '200 OK')

    def test_user_login_fail(self):
        with self.app.app_context():
            with self.app.test_request_context():
                with self.app.test_client() as c:
                    new_user = c.post('/api/users', data=self.valid_user_data)

                    response = c.post('/api/users/login',
                                      data=self.invalid_login_data_password_bad)
                    status = response.status
                    data = response.data.decode('utf-8')
                    data = json.loads(data)
                    self.assertEqual(status, '401 UNAUTHORIZED')

    def test_user_login_fail_no_user(self):
        with self.app.app_context():
            with self.app.test_request_context():
                with self.app.test_client() as c:

                    response = c.post('/api/users/login',
                                      data=self.invalid_login_data_password_bad)
                    status = response.status
                    data = response.data.decode('utf-8')
                    data = json.loads(data)
                    self.assertEqual(status, '400 BAD REQUEST')

    def tearDown(self):
        user.User.drop_collection()


if __name__ == '__main__':
    unittest.main()
