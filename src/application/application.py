from flask import send_file
from flask_restful import Resource, reqparse
from werkzeug.datastructures import FileStorage

from os.path import exists

from src.utils.es_interface import ElasticInterface, MockElasticInterface
from src.utils.io_interface import InputOutputInterface
from src.utils.log import get_default_logger

ARG_FILE_ID = 'file_id'
ARG_FILE = 'file'
ARG_FILE_NAME = 'file_name'
ARG_DELETED_FILE_ID = 'deleted_file_id'

ENV = 'env'
ENV_DEV = 'dev'
ENV_TEST = 'test'
ENV_PROD = 'prod'


class Application(Resource):

    def __init__(self, env=ENV_PROD):
        super().__init__()
        self._log = get_default_logger(self)

        if env == ENV_DEV:
            self.es = ElasticInterface(host="0.0.0.0")
        elif env == ENV_PROD:
            self.es = ElasticInterface()
        else:
            # For unit testing purposes, we don't spin up an ES cluster
            self.es = MockElasticInterface()

        self.io = InputOutputInterface()

    def get(self):
        """
        Return a file to the client, given a document ID
        """
        parser = reqparse.RequestParser()
        parser.add_argument(ARG_FILE_ID, type=str, help='The ID for the file stored in ElasticSearch')
        args = parser.parse_args()

        try:
            file_id = args[ARG_FILE_ID]
        except KeyError:
            return '', 400

        # Hacky way to ping the server :)
        if file_id == 'ping':
            return 'pong', 200

        file_path = self.es.search_filename_by_id(file_id)

        if file_path is None:
            return 404

        if exists(file_path):
            return send_file(file_path)
        else:
            return '', 404

    def delete(self):
        """ Delete a file from the server"""
        parser = reqparse.RequestParser()
        parser.add_argument(ARG_FILE_ID, type=str, help='The ID for the file stored in ElasticSearch')
        args = parser.parse_args()
        file_id = args[ARG_FILE_ID]
        try:
            file_name = self.es.delete_file_by_id(file_id)
            self.io.delete_file(file_name)
        except FileNotFoundError:
            return f'File with id {file_id} not found', 404

        return {
            ARG_DELETED_FILE_ID: file_id,
            ARG_FILE_NAME: file_name
        }

    def put(self):
        """ PUT means insert, replace if already exists """
        parser = reqparse.RequestParser()
        parser.add_argument(ARG_FILE, location='files', type=FileStorage, help='The file to be stored')

        args = parser.parse_args()
        input_file = args[ARG_FILE]

        file_id = self.es.search_id_by_filename(input_file.filename)
        if file_id is not None:
            self._log.info(f'{input_file.filename} exists. Updating {file_id}')

        file_id = self.es.add_document_details(input_file.filename, file_id=file_id)
        self.io.save_file(input_file)
        return {ARG_FILE_ID: file_id}
