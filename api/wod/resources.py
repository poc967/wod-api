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
    parser.add_argument('date')
    parser.add_argument('workoutComponents', action='append')
    return parser


def get_time_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('time_stamp', type=int, location='args')
    return parser


@api.route('', '/', '/<int:time_stamp>')
@api.param('time_stamp', 'unix time stamp')
class Wod(Resource):

    @flask_login.login_required
    def post(self):
        parser = create_wod_parser()
        args = parser.parse_args()

        return controllers.create_wod(args)

    @flask_login.login_required
    def get(self, time_stamp):

        return controllers.get_wods(time_stamp)


# @api.route('/<current_time>')
# @api.param('current_time', 'current time from client')
# class WodByTime(Resource):
#     def get(self, current_time):

#         return controllers.get_wods(current_time)
