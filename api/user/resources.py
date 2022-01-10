import flask_login
from flask import request
from flask_restx import reqparse
from flask_restx import Namespace, Resource, Api
from ..models import user
import bcrypt
from .controllers import create_user

api = Namespace('users')


def create_user_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('first_name')
    parser.add_argument('last_name')
    parser.add_argument('email')
    parser.add_argument('password')
    return parser


def login_user_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('email')
    parser.add_argument('password')
    return parser


@api.route('')
class CreateUser(Resource):

    def post(self):
        parser = create_user_parser()
        args = parser.parse_args()

        # if not args['email'] or args['first_name'] or args['last_name'] or args['password']:
        #     return {
        #         'error': 'missing required arguments'
        #     }, 400

        response = create_user(args)

        return response


@api.route('/<user_id>')
@api.param('user_id', 'the user id')
class UserById(Resource):

    def delete(self, user_id):

        if not user_id:
            return {
                'error': 'missing required parameter id'
            }, 400

        user_to_delete = user.User.objects(id=user_id).first()

        if not user_to_delete:
            return {
                'error': 'user does not exist'
            }, 400

        user_to_delete.delete_user()

        return {
            'success': 'user successfully deleted'
        }, 200


@api.route('/logout')
class LogOutUser(Resource):
    def get(self):

        flask_login.logout_user()

        return {
            'data': 'user logged out successfully'
        }, 200


@api.route('/login')
class LogInUser(Resource):
    def post(self):

        parser = login_user_parser()
        args = parser.parse_args()

        user_to_authenticate = user.User.objects(email=args['email']).first()

        if not user_to_authenticate:
            return {
                'error': 'user does not exist with this email'
            }, 401

        result = bcrypt.checkpw(
            args['password'].encode('utf-8'), user_to_authenticate.password.encode('utf-8'))

        if not result:
            return {
                'error': 'incorrect password'
            }, 401
        else:
            flask_login.login_user(user_to_authenticate)
            return {
                'data': user_to_authenticate.user_to_json()
            }, 200
