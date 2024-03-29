import flask_login
import mongoengine
import datetime

# TODO add model for benchmark lifts


class User(mongoengine.Document, flask_login.UserMixin, flask_login.AnonymousUserMixin):
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
    profile_picture = mongoengine.StringField()
    is_active = mongoengine.BooleanField(default=True)
    created = mongoengine.DateTimeField(default=datetime.datetime.now())

    @property
    def is_authenticated(self):
        return True

    def delete_user(self):
        self.is_active = False
        self.save()
        return

    def user_to_json(self):
        data = {
            'id': str(self.id),
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_active': self.is_active,
            'profile_picture': self.profile_picture
        }

        return data
