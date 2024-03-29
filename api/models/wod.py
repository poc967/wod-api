import mongoengine
from api.models import movement, work_out
import datetime


def get_work_out_object(work_out_id):
    work_out_object = work_out.WorkOut.objects(id=work_out_id).first()
    return work_out_object


class Wod(mongoengine.Document):
    title = mongoengine.StringField()
    date = mongoengine.DateField()
    users = mongoengine.ListField(mongoengine.ReferenceField('User'))
    work_outs = mongoengine.ListField(mongoengine.ReferenceField('WorkOut'))

    def wod_to_json(self):
        data = {
            'title': self.title,
            'date': self.date.strftime("%c") if self.date else None,
            'work_outs': [get_work_out_object(work_out_document.id).work_out_to_json() for work_out_document in self.work_outs]
        }

        return data
