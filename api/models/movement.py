import mongoengine
import datetime


class Movement(mongoengine.Document):
    name = mongoengine.StringField()
    is_deleted = mongoengine.BooleanField(default=False)
    created = mongoengine.DateTimeField(default=datetime.datetime.now())

    def find_or_create_movement(movement):
        name = movement.lower()
        result_of_movement_query = Movement.objects(
            name=name).first()
        if not result_of_movement_query:
            new_movement = Movement(
                name=name)
            new_movement.save()
        else:
            new_movement = result_of_movement_query
        return new_movement

    def movement_to_json(self):
        data = {
            'id': str(self.id),
            'name': self.name,
            'is_deleted': self.is_deleted,
            'created': self.created.strftime("%c")
        }

        return data
