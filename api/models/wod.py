import mongoengine
from api.models import movement, work_out


def get_work_out_object(work_out_id):
    work_out_object = work_out.WorkOut.objects(id=work_out_id).first()
    return work_out_object


class Wod(mongoengine.Document):
    name = mongoengine.StringField()
    work_outs = mongoengine.ListField(mongoengine.ReferenceField('WorkOut'))

    def wod_to_json(self):
        work_out_documents = []
        for ids in self.work_outs:
            document = get_work_out_object(ids)
            work_out_documents.append(document)

        data = {
            'name': self.name,
            'work_outs': [work_out_document.work_out_to_json() for work_out_document in work_out_documents]
        }

        return {'data': data}, 200
