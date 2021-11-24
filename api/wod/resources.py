from flask_restx import Namespace, Api, Resource
from flask_restx import reqparse
from ..models import wod

api = Namespace('wod')

@api.route('/')
class Wod(Resource):
    def get(self):
        return {
            'message': 'routing is cool!'
        }, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        args = parser.parse_args()

        new_wod = wod.Wod(name=args['name'])
        new_wod.save()
        return 201

