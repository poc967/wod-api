from ..models import wod, work_out, movement
import ast
import datetime


def create_wod(args):
    new_wod = wod.Wod(title=args['title'], date=datetime.datetime.now())

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
    new_wod.reload()
    return new_wod.wod_to_json(), 201


def get_wods(timestamp=None):
    today = datetime.date.fromtimestamp(timestamp)
    start = datetime.datetime(today.year, today.month,
                              today.day, 0).astimezone()
    end = start + datetime.timedelta(1)

    try:
        wods = wod.Wod.objects(date__gte=start, date__lt=end).all()
        return {'data': [wod.wod_to_json() for wod in wods], 'count': len(wods)}
    except Exception as e:
        return {'error': str(e)}, 400
