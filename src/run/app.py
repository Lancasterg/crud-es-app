from flask import Flask
from flask_restful import Api

from src.application.application import Application, ENV, ENV_PROD, ENV_DEV


def build_app(env=ENV_PROD):
    app = Flask(__name__)
    app.config['UPLOADS_FOLDER'] = '/tmp/www/'
    app.config['TESTING'] = False if env in [ENV_DEV, ENV_PROD] else True
    api = Api(app)
    api.add_resource(Application, '/', resource_class_kwargs={ENV: env})
    return app


app = build_app()
