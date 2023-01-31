from ..models import user
import flask_login
import bcrypt
import boto3
import io
import bson
import uuid


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


def update_user(args, user_id):
    s3 = boto3.client('s3')
    file = args['image'].read()
    bytes = io.BytesIO(file)

    file_id = str(uuid.uuid4())

    error = s3.upload_fileobj(
        bytes, 'wod-tracker-profile', file_id, ExtraArgs={'ACL': 'public-read'})

    if error:
        return {
            'error': 'file could not be uploaded'
        }, 400

    url = f'https://wod-tracker-profile.s3.amazonaws.com/{file_id}'

    user_to_update = user.User.objects(id=user_id).first()
    if not user_to_update:
        return {
            'error': 'no user found'
        }, 400

    user_to_update.profile_picture = url
    user_to_update.save()
    return {
        'data': user_to_update.user_to_json()
    }, 200
