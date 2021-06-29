from flask import Flask
from flask_restful import Api

from src.application.application import Application

app = Flask(__name__)
app.config['UPLOADS_FOLDER'] = '/tmp/www/'
app.config['TESTING'] = False
api = Api(app)
debug = True
host = "0.0.0.0"
api.add_resource(Application, '/', resource_class_kwargs={'env': 'test'})


def main():
    app.run(host=host, debug=debug)


if __name__ == '__main__':
    main()
