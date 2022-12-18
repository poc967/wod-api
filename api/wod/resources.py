from flask_restx import Namespace, Api, Resource
from flask_restx import reqparse
from ..models import wod, work_out, movement
import ast
import flask_login
import logging
from . import controllers

api = Namespace('wod')


def create_wod_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('title')
    parser.add_argument('workoutComponents', action='append')
    return parser


@api.route('')
class Wod(Resource):

    @flask_login.login_required
    def post(self):
        parser = create_wod_parser()
        args = parser.parse_args()

        return controllers.create_wod(args)

    @flask_login.login_required
    def get(self):

        results = wod.Wod.objects()
        return [result.wod_to_json() for result in results]


@api.route('/<current_time>')
@api.parem('current_time', 'current time from client')
class WodByTime(Resource):
    def get(self, current_time):
