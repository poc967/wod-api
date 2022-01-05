import flask_login
import mongoengine
import datetime

# TODO add model for benchmark lifts


class User(mongoengine.Document, flask_login.UserMixin):
    first_name = mongoengine.StringField()
    last_name = mongoengine.StringField()
    age = mongoengine.IntField()
    weight = mongoengine.FloatField()
    height_feet = mongoengine.IntField()
    height_inches = mongoengine.IntField(max_value=12)
    updated = mongoengine.DateTimeField()
    email = mongoengine.StringField(unique=True)
    password = mongoengine.StringField()
    benchmark_lifts = mongoengine.ListField()
    is_deleted = mongoengine.BooleanField(default=False)
    created = mongoengine.DateTimeField(default=datetime.datetime.now())

    def user_loader(id):
        found_user = User.objects(id=id).first()

        if not found_user:
            return None
        else:
            return found_user
