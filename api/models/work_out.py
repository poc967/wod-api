from enum import unique
import mongoengine
import datetime
from mongoengine.fields import StringField
from api.models.movement import Movement
class WorkOut(mongoengine.Document):
    work_out_style = mongoengine.StringField()
    time_domain = mongoengine.StringField()
    rounds = mongoengine.IntField()
    movements = mongoengine.EmbeddedDocumentListField(Movement)
    score = mongoengine.StringField()
    notes = mongoengine.StringField()
    is_deleted = mongoengine.BooleanField(default=False)
    created = mongoengine.DateTimeField(default=datetime.datetime.now())

    def work_out_to_json(self):
        data = {
            'id': str(self.id),
            'time_domain': self.time_domain,
            'is_deleted': self.is_deleted,
            'rounds': self.rounds if self.rounds else None,
            'movements': self.movements,
            'score': self.score,
            'notes': self.score,
            'created': self.created.strftime("%c")
        }

        return data