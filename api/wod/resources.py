from flask_restx import Namespace, Api, Resource

api = Namespace('wod')

@api.route('/')
class Wod(Resource):
    def get(self):
        return {
            'message': 'routing is cool!'
        }, 200