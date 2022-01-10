from ..models import user
import flask_login
import bcrypt


def create_user(args):
    found_user = user.User.objects(email=args['email'])

    if found_user:
        return {
            'error': f'user associated with this email ({args["email"]}) already exists'
        }, 400

    new_user = {
        'first_name': args['first_name'],
        'last_name': args['last_name'],
        'email': args['email']
    }

    new_user = user.User(**new_user)

    hashed_password = bcrypt.hashpw(
        args['password'].encode('utf-8'), bcrypt.gensalt())

    new_user.password = hashed_password.decode('utf-8')
    new_user.save()

    # authenticate user
    flask_login.login_user(new_user)

    return {
        'data': new_user.user_to_json()
    }, 201
