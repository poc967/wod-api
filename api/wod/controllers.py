from ..models import wod, work_out, movement
import ast


def create_wod(args):
    new_wod = wod.Wod(title=args['title'])

    for component in args['workoutComponents']:
        component = ast.literal_eval(component)
        movements = []

        for single_movement in component['movements']:
            new_movement = movement.Movement.find_or_create_movement(
                single_movement['movement'])

            new_workout_movement_args = {
                'movement': new_movement.id,
                'repititions': single_movement['repititions'],
                'weight': single_movement['weight']
            }

            movements.append(work_out.WorkOutMovement(
                **new_workout_movement_args))

        component_args = {
            'description': component['description'],
            'notes': component['notes'],
            'movements': movements
        }

        new_work_out_movement = work_out.WorkOut(**component_args)
        new_work_out_movement.save()

        new_wod.work_outs.append(new_work_out_movement.id)

    new_wod.save()
    return new_wod.wod_to_json(), 201
