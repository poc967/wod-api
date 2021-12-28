import mongoengine
import datetime


class Wod(mongoengine.Document):
    first_name = mongoengine.StringField()
    last_name = mongoengine.StringField()
    email = mongoengine.StringField(unique=True)
    password = mongoengine.StringField()
    benchmark_lifts = mongoengine.ListField()
    is_deleted = mongoengine.BooleanField(default=False)
    created = mongoengine.DateTimeField(default=datetime.datetime.now())
