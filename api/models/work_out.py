from enum import unique
import mongoengine
import datetime
from mongoengine.fields import StringField
from api.models import movement
from api.models.movement import Movement


def get_movement_document(movement_id):
    movement_document = Movement.objects(id=movement_id).first()
    return movement_document


class WorkOutMovement(mongoengine.EmbeddedDocument):
    movement = mongoengine.ObjectIdField()
    repititions = mongoengine.StringField()
    sets = mongoengine.IntField()
    weight = mongoengine.StringField()
    notes = mongoengine.StringField()

    def work_out_movement_to_json(self):
        movement_document = get_movement_document(self.movement)

        return {
            'movement': movement_document.movement_to_json(),
            'repititions': self.repititions,
            'sets': self.sets,
            'weight': self.weight,
            'notes': self.notes
        }


class WorkOut(mongoengine.Document):
    work_out_style = mongoengine.StringField(
        choices=['AMRAP', 'For Time', 'EMOM'])
    time_cap = mongoengine.StringField()
    rounds = mongoengine.IntField()
    repititions = mongoengine.StringField()
    movements = mongoengine.EmbeddedDocumentListField(WorkOutMovement)
    notes = mongoengine.StringField()
    is_deleted = mongoengine.BooleanField(default=False)
    created = mongoengine.DateTimeField(default=datetime.datetime.now())

    def work_out_to_json(self):

        data = {
            'id': str(self.id),
            'work_out_style': self.work_out_style,
            'time_cap': self.time_cap,
            'is_deleted': self.is_deleted,
            'rounds': self.rounds if self.rounds else None,
            'movements': [movement.work_out_movement_to_json() for movement in self.movements],
            'repititions': self.repititions,
            'notes': self.notes,
            'created': self.created.strftime("%c")
        }

        return data
