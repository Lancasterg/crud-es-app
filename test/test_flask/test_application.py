from flask import Flask
from flask_restful import Api
from unittest import TestCase

from src.application.application import Application


class TestApplication(TestCase):

    def setUp(self):
        app = Flask(__name__)
        api = Api(app)
        api.add_resource(Application, '/', resource_class_kwargs={'env': 'test'})
        self.client = app.test_client()

    def test_ping(self):
        r = self.client.get("/?file_id=ping")
        self.assertEqual(r.status_code, 200)

    def test_put_then_get(self):
        pass
