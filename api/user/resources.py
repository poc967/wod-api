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

        if not args.get('email') or not args.get('first_name') or not args.get('last_name') or not args.get('password'):
            return {
                'error': 'missing required arguments'
            }, 400

        response = create_user(args)

        return response


@api.route('/current_user')
class GetCurrentUser(Resource):

    # @flask_login.login_required
    def get(self):
        user = flask_login.current_user
        print(user.is_authenticated, type(user))

        if not user.is_authenticated:
            return {
                'error': 'user not authed'
            }, 401
        else:
            return {
                'data': user.user_to_json()
            }, 200


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

    def get(self, user_id):

        if not user_id:
            return {
                'error': 'missing required parameter id'
            }, 400

        found_user = user.User.objects(id=user_id).first()

        if not found_user:
            return {
                'error': 'no user found'
            }, 400

        return {
            'data': found_user.user_to_json()
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
            }, 400

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
