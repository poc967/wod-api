from flask_restx import Namespace, Api, Resource
from flask_restx import reqparse
from ..models import movement

api = Namespace('movement')

@api.route('/')
class CreateMovement(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        parser.add_argument('notes', action='append')
        args = parser.parse_args()

        new_movement = movement.Movement(name=args['name'], notes=args['notes'])
        new_movement.save()

        return new_movement.to_json()

        