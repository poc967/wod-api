from flask import Flask
from flask_restx import Api
from flask_mongoengine import MongoEngine
from api.work_out.resources import api as work_outs
from api.wod.resources import api as wods
from api.movement.resources import api as movements
from api.user.resources import api as users
from api.models import user
import flask_login

app = Flask(__name__)
api = Api(app, prefix='/api')

login_manager = flask_login.LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def user_loader(id):
    found_user = user.User.objects(id=id).first()

    if not found_user:
        return None
    else:
        return found_user


app.config['MONGODB_SETTINGS'] = {
    "db": "wod-api",
    "host": "mongodb://localhost:27017/wod-api"
}
app.secret_key = 'supersecret'
db = MongoEngine(app)

api.add_namespace(wods, path='/wod')
api.add_namespace(movements, path='/movement')
api.add_namespace(work_outs, path='/work-out')
api.add_namespace(users, path='/users')

if __name__ == '__main__':
    app.run(debug=True)
