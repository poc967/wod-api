from flask_restx import Namespace, Api, Resource
from flask_restx import reqparse
from ..models import wod, work_out, movement
import ast

api = Namespace('wod')


def create_wod_parser():
    parser = reqparse.RequestParser()
    parser.add_argument('name')
    parser.add_argument('work_outs', action='append')
    return parser


@api.route('')
class Wod(Resource):
    def post(self):
        parser = create_wod_parser()
        args = parser.parse_args()

        new_wod = wod.Wod(name=args['name'])

        work_out_components = args['work_outs']
        for work_out_component in work_out_components:
            work_out_component = ast.literal_eval(work_out_component)

            new_work_out_component = work_out.WorkOut(
                work_out_style=work_out_component['work_out_style'] if work_out_component.get(
                    'work_out_style') else None,
                time_cap=work_out_component['time_cap'] if work_out_component.get(
                    'time_cap') else None,
                rounds=work_out_component['rounds'] if work_out_component.get(
                    'rounds') else None,
                notes=work_out_component['notes'] if work_out_component.get(
                    'notes') else None,
                repititions=work_out_component['repititions'] if work_out_component.get(
                    'repititions') else None
            )

            for individual_movement in work_out_component['movements']:
                new_movement = movement.Movement.find_or_create_movement(
                    individual_movement)

                new_work_out_component['movements'].append(work_out.WorkOutMovement(
                    movement=new_movement,
                    repititions=individual_movement['repititions'] if individual_movement.get(
                        'repititions') else None,
                    notes=individual_movement['notes'] if individual_movement.get(
                        'notes') else None,
                    weight=individual_movement['weight'] if individual_movement.get(
                        'weight') else None,
                    sets=individual_movement['sets'] if individual_movement.get(
                        'sets') else None
                )
                )

            new_work_out_component.save()

            new_wod['work_outs'].append(new_work_out_component.id)

        new_wod.save()

        return new_wod.wod_to_json(), 201
