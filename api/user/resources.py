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


@api.route('')
class CreateUser(Resource):
    def post(self):
        parser = create_user_parser()
        args = parser.parse_args()

        found_user = user.User.objects(email=args['email'])

        if found_user:
            return {
                'error': f'user associated with this email (${found_user.email}) already exists'
            }, 400

        new_user = {
            'first_name': args['first_name'],
            'last_name': args['last_name'],
            'email': args['email']
        }

        new_user = user.User(**new_user)
        print(args['password'])

        hashed_password = bcrypt.hashpw(
            args['password'].encode('utf-8'), bcrypt.gensalt())

        new_user['password'] = hashed_password
        new_user.save()
        return 201
