from flask import Flask
from flask_restx import Api
from flask_mongoengine import MongoEngine
from api.wod.resources import api as wods
from api.movement.resources import api as movements

app = Flask(__name__)
api = Api(app, prefix='/api')

app.config['MONGODB_SETTINGS'] = {
    "db": "wod-api",
    "host": "mongodb://localhost:27017/wod-api"
}
db = MongoEngine(app)

api.add_namespace(wods, path='/wod')
api.add_namespace(movements, path='/movement')

if __name__ == '__main__':
    app.run(debug=True)