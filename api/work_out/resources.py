from os import name
from flask_restx import Namespace, Api, Resource
from flask_restx import reqparse
from mongoengine.errors import NotUniqueError
from ..models import movement, work_out

api = Namespace('work-out')


@api.route('/')
class CreateMovement(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('work_out_style')
        parser.add_argument('time_domain')
        parser.add_argument('rounds')
        parser.add_argument('score')
        parser.add_argument('notes')
        parser.add_argument('movement')
        args = parser.parse_args()

        new_movement = movement.Movement(name=args['movement'])
        new_movement.save()
        print(new_movement.id)
        new_work_out_movement = work_out.WorkOutMovement(
            movement=new_movement.id, repititions=4)
        print(new_work_out_movement)

        new_work_out = work_out.WorkOut(
            work_out_style=args['work_out_style'], time_domain=args['time_domain'], rounds=args['rounds'], movements=[new_work_out_movement])
        print(new_work_out)
        new_work_out.save()

        return {'data': new_work_out.work_out_to_json()}, 201
