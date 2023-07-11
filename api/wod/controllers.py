from ..models import wod, work_out, movement
import ast
import datetime
from flask_login import current_user


def create_wod(args):
    date = datetime.datetime.strptime(
        args['date'], "%Y-%m-%dT%H:%M:%S.%fZ") if args.get('date') else None
    new_wod = wod.Wod(
        title=args['title'], date=date if args.get('date') else None, users=[current_user])

    for workout in args['workoutComponents']:
        dict = ast.literal_eval(workout)
        new_workout_component = work_out.WorkOut(
            description=dict.get('data'),
            results=dict.get('resultType').lower(),
            result_sets=str(dict.get('resultSets'))
        )
        new_workout_component.save()
        new_wod.work_outs.append(new_workout_component)

    new_wod.save()
    return {'message': 'success'}, 201


def get_wods(timestamp=None):
    today = datetime.date.fromtimestamp(timestamp)
    start = datetime.datetime(today.year, today.month,
                              today.day, 0).astimezone()
    end = start + datetime.timedelta(1)

    try:
        wods = wod.Wod.objects(
            date__gte=start, date__lt=end, users__in=[current_user]).all()
        return {'data': [wod.wod_to_json() for wod in wods], 'count': len(wods)}
    except Exception as e:
        return {'error': str(e)}, 400
