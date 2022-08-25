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
    description = mongoengine.StringField()
    work_out_style = mongoengine.StringField(
        choices=['AMRAP', 'For Time', 'EMOM', 'Other'])
    time_cap = mongoengine.StringField()
    interval_time_domain = mongoengine.StringField()
    rounds = mongoengine.IntField()
    rep_scheme = mongoengine.StringField()
    movements = mongoengine.EmbeddedDocumentListField(WorkOutMovement)
    notes = mongoengine.StringField()
    is_deleted = mongoengine.BooleanField(default=False)
    created = mongoengine.DateTimeField(default=datetime.datetime.now())

    def work_out_to_json(self):

        data = {
            'id': str(self.id),
            'description': self.description,
            'is_deleted': self.is_deleted,
            'movements': [movement.work_out_movement_to_json() for movement in self.movements],
            'notes': self.notes,
            'created': self.created.strftime("%c")
        }

        return data

    def create_new_workout(args):

        return
