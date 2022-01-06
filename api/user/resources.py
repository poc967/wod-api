import flask_login
from flask_restx import reqparse
from flask_restx import Namespace, Resource, Api
from ..models import user
import bcrypt

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
        from app import user_loader
        parser = create_user_parser()
        args = parser.parse_args()

        found_user = user.User.objects(email=args['email'])

        if found_user:
            return {
                'error': f'user associated with this email ({args["email"]}) already exists'
            }, 400

        new_user = {
            'first_name': args['first_name'],
            'last_name': args['last_name'],
            'email': args['email']
        }

        new_user = user.User(**new_user)

        hashed_password = bcrypt.hashpw(
            args['password'].encode('utf-8'), bcrypt.gensalt())

        new_user.password = hashed_password.decode('utf-8')
        new_user.save()

        # authenticate user
        flask_login.login_user(new_user)

        return {
            'data': new_user.user_to_json()
        }, 201


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
