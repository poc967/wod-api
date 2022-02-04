from flask import Flask
from flask_restx import Api
from flask_mongoengine import MongoEngine
from api.work_out.resources import api as work_outs
from api.wod.resources import api as wods
from api.movement.resources import api as movements
from api.user.resources import api as users
from api.models import user
import flask_login
from flask_cors import CORS


def create_app(test_mode=None):
    """
    application factory

    """
    app = Flask(__name__)
    api = Api(app, prefix='/api')
    CORS(app, origins=['http://localhost:3000'], supports_credentials=True)
    if app.env == 'production':
        app.config['MONGODB_SETTINGS'] = {
            "db": "wod-api",
            "host": "mongodb://localhost:27017/wod-api"
        }
        app.secret_key = 'supersecret'
    elif app.env == 'development' or test_mode == 'testing':
        app.config['MONGODB_SETTINGS'] = {
            "db": "test-wod-api",
            "host": "mongodb://localhost:27017/test-wod-api"
        }
        app.secret_key = 'supersecret'

    db = MongoEngine(app)

    login_manager = flask_login.LoginManager()
    login_manager.init_app(app)

    api.add_namespace(wods, path='/wod')
    api.add_namespace(movements, path='/movement')
    api.add_namespace(work_outs, path='/work-out')
    api.add_namespace(users, path='/users')

    @login_manager.user_loader
    def user_loader(user_id):
        found_user = user.User.objects(id=user_id).first()

        if not found_user:
            return None
        else:
            return found_user

    # @login_manager.unauthorized_handler
    # def unauthorized():
    #     return None

    # @login_manager.request_loader
    # def request_loader():

    if __name__ == '__main__':
        app.run(debug=True)

    return app
