from flask_restx import Namespace, Api, Resource
from flask_restx import reqparse
from mongoengine.errors import NotUniqueError
from ..models import movement

api = Namespace('movement')


def create_movement_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('name')
    return parser


@api.route('/')
class CreateMovement(Resource):
    def post(self):
        parser = create_movement_parser()
        args = parser.parse_args()

        args['name'] = args['name'].lower()
        try:
            new_movement = movement.Movement(name=args['name'])
            new_movement.save()
        except NotUniqueError:
            return {'error': 'This movement already exists'}, 400
        except Exception as e:
            return {'error': str(e)}, 400

        return {'data': new_movement.movement_to_json()}, 201

    def get(self):
        movements = movement.Movement.objects(is_deleted=False)

        if not movements:
            return {'error': 'An error occured while fetching movements'}, 400

        return {
            'data': [movement.movement_to_json() for movement in movements]
        }, 200
