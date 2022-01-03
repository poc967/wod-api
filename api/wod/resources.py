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

            # build dict for creating work out components
            kwargs = {}
            base_required_fields = [
                'work_out_style', 'description', 'movements']

            for field in base_required_fields:
                if not work_out_component.get(field):
                    return {
                        'error': f'Missing required field {field}'
                    }, 400
                else:
                    if field != 'movements':
                        kwargs[field] = work_out_component[field]

            secondary_required_fields = []

            if work_out_component['work_out_style'] == 'AMRAP':
                secondary_required_fields.extend(['time_cap'])
            elif work_out_component['work_out_style'] == 'For Time':
                secondary_required_fields.append('time_cap')
            elif work_out_component['work_out_style'] == 'EMOM':
                secondary_required_fields.extend(
                    ['time_cap', 'interval_time_domain'])

            for field in secondary_required_fields:
                if not work_out_component.get(field):
                    return {
                        'error': f'Missing required field {field}'
                    }, 400
                else:
                    kwargs[field] = work_out_component[field]

            optional_fields = []

            for field in work_out_component:
                if field not in secondary_required_fields or base_required_fields:
                    optional_fields.append(field)

            if len(optional_fields) > 0:
                for field in optional_fields:
                    if field != 'movements':
                        kwargs[field] = work_out_component[field]

            new_work_out_component = work_out.WorkOut(**kwargs)

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
