import mongoengine
from api.models import movement, work_out
import datetime


def get_work_out_object(work_out_id):
    work_out_object = work_out.WorkOut.objects(id=work_out_id).first()
    return work_out_object


class Wod(mongoengine.Document):
    title = mongoengine.StringField()
    date = mongoengine.DateField()
    work_outs = mongoengine.ListField(mongoengine.ReferenceField('WorkOut'))

    def wod_to_json(self):
        print(self.work_outs)
        data = {
            'title': self.title,
            'date': self.date.strftime("%c"),
            'work_outs': [get_work_out_object(work_out_document.id).work_out_to_json() for work_out_document in self.work_outs]
        }

        return data
