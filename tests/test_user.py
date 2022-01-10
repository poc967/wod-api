import unittest

from flask_mongoengine import MongoEngine

from api.user.controllers import create_user
from api.models import user
from app import create_app
import flask


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

        return

    def test_create_user_success(self):
        with self.app.app_context():
            with self.app.test_request_context():
                response = create_user(self.valid_user_data)

                # jsonify
                (data, status) = response
                self.assertEquals(status, 201)

    def tearDown(self):
        user.User.drop_collection()


if __name__ == '__main__':
    unittest.main()
