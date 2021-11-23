from flask import Flask
from flask_restx import Api
from api.wod.resources import api as wods

app = Flask(__name__)
api = Api(app, prefix='/api')

api.add_namespace(wods, path='/wod')

if __name__ == '__main__':
    app.run(debug=True)