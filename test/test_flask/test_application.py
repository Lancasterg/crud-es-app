import io

from flask import Flask, url_for
from flask_restful import Api
from unittest import TestCase

from werkzeug.datastructures import FileStorage

from src.application.application import Application, ENV_TEST, ENV


class TestApplication(TestCase):

    def setUp(self):
        app = Flask(__name__)
        api = Api(app)
        api.add_resource(Application, '/', resource_class_kwargs={ENV: ENV_TEST})
        self.client = app.test_client()

    def test_ping(self):
        r = self.client.get("/?file_id=ping")
        self.assertEqual(r.status_code, 200)

    def test_get_fail(self):
        r = self.client.get("/?file_id=file_doesnt_exist")
        self.assertEqual(r.status_code, 404)

    def test_put_then_get(self):
        data = {'file': (io.BytesIO(b"abcdef"), 'test.jpg')}
        r = self.client.put(url_for('/'), data=data, content_type='multipart/form-data', follow_redirects=True)
        print(r)
