import mongoengine

class Wod(mongoengine.Document):
    name = mongoengine.StringField()
