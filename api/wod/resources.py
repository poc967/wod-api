from flask_restx import Namespace, Api, Resource
from flask_restx import reqparse
from ..models import wod, work_out, movement
import json
import ast

api = Namespace('wod')


@api.route('/')
class Wod(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name')
        parser.add_argument('score')
        parser.add_argument('work_outs', action='append')
        args = parser.parse_args()

        new_wod = wod.Wod(name=args['name'], score=args['score'])

        work_outs = args['work_outs']
        for sub_work_out in work_outs:
            sub_work_out = ast.literal_eval(sub_work_out)

            new_work_out = work_out.WorkOut(
                work_out_style=sub_work_out['work_out_style'],
                time_domain=sub_work_out['time_domain'],
                score=sub_work_out['score'],
                notes=sub_work_out['notes']
            )

            for individual_movement in sub_work_out['movements']:
                result_of_movement_query = movement.Movement.objects(
                    name=individual_movement['movement'].lower()).first()
                if not result_of_movement_query:
                    new_movement = movement.Movement(
                        name=individual_movement['movement'].lower()
                    )
                    new_movement.save()
                    new_movement = new_movement.id
                else:
                    new_movement = result_of_movement_query.id

                new_work_out['movements'].append(work_out.WorkOutMovement(
                    movement=new_movement,
                    repititions=individual_movement['repititions'],
                    notes=individual_movement['notes']
                )
                )

            new_work_out.save()

            new_wod['work_outs'].append(new_work_out.id)

        new_wod.save()

        return new_wod.wod_to_json(), 201
