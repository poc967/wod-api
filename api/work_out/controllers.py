from ..models import work_out


def create_result(args):
    # verify we have the needed args
    results = args.get('results')
    notes = args.get('notes')
    workout_id = args.get('workout_id')
    if not results:
        return {'error', 'missing results'}, 400

    if not workout_id:
        return {'error': 'no workout id supplied'}, 400

    # lookup the workout the result belongs to
    workout = work_out.WorkOut.objects(id=workout_id).first()
    if not workout:
        return {'error': 'workout cannot be found'}, 400

    # set the list of results and the notes on the doc
    kwargs = {
        'workout_id': workout.id,
        'notes': notes,
        'results': results
    }

    new_result = work_out.Result(**kwargs)
    new_result.save()

    return {'success': 'result has been saved'}, 201
