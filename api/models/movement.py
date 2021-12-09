from enum import unique
import mongoengine
import datetime


class Movement(mongoengine.Document):
    name = mongoengine.StringField()
    is_deleted = mongoengine.BooleanField(default=False)
    created = mongoengine.DateTimeField(default=datetime.datetime.now())

    def movement_to_json(self):
        data = {
            'id': str(self.id),
            'name': self.name,
            'is_deleted': self.is_deleted,
            'created': self.created.strftime("%c")
        }

        return data
