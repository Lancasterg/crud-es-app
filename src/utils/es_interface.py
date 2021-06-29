from elasticsearch import Elasticsearch, RequestError
from typing import Dict
import json
from src.utils.log import get_default_logger
from src.utils.io_interface import InputOutputInterface
from abc import ABC, abstractmethod


class AbstractElasticInterface(ABC):
    DEFAULT_INDEX = 'file_index'
    DISK_LOCATION = 'location_on_disk'
    HITS = 'hits'
    ID = '_id'
    SOURCE = '_source'

    @abstractmethod
    def delete_file_by_id(self, file_id):
        raise NotImplementedError()

    @abstractmethod
    def add_document_details(self, file_path, file_id=None):
        raise NotImplementedError()

    @abstractmethod
    def search_filename_by_id(self, file_id, index=DEFAULT_INDEX):
        raise NotImplementedError()

    @abstractmethod
    def search_id_by_filename(self, file_name, index=DEFAULT_INDEX):
        raise NotImplementedError()


class MockElasticInterface(AbstractElasticInterface):
    """
    Mock class for testing without spinning up an ES cluster
    """

    def __init__(self):
        self.fake_es = {}
        self.io = InputOutputInterface()

    def search_filename_by_id(self, file_id, index=AbstractElasticInterface.DEFAULT_INDEX):
        try:
            return self.fake_es[file_id]
        except KeyError:
            return None

    def search_id_by_filename(self, file_name, index=AbstractElasticInterface.DEFAULT_INDEX):
        for key, value in self.fake_es.items():
            if value == file_name:
                return value
        return None

    def add_document_details(self, file_path, file_id=None):
        # Search for existing file
        tmp_file_id = self.search_id_by_filename(file_path)
        if file_id is None or tmp_file_id is None:
            file_id = self.io.generate_id()
        self.fake_es[file_id] = file_path
        return file_id

    def delete_file_by_id(self, file_id):
        try:
            file_name = self.fake_es[file_id]
            del self.fake_es[file_id]
            return file_name
        except KeyError:
            return None


class ElasticInterface(AbstractElasticInterface):

    def __init__(self, host='0.0.0.0', port=9200):
        self.es = Elasticsearch([{'host': host, 'port': port}])

        # If we haven't yet instantiated the file_index, do so now
        if not self.es.indices.exists(index="file_index"):
            self.es.indices.create(index='file_index')

        self.io = InputOutputInterface()
        self._log = get_default_logger(__class__.__name__)

    def delete_file_by_id(self, file_id):
        """
        Given a file id, delete the id from ElasticSearch
        TODO: handle error when file not found

        :param file_id: The file id to delete
        :return:
        """
        result = self.search_filename_by_id(file_id)
        if result is not None:
            self.es.delete(index=self.DEFAULT_INDEX, id=file_id)
        return result

    def add_document_details(self, file_path, file_id=None):
        """
        Public wrapper method for _add_document_details

        :param file_path:
        :param file_id:
        :return:
        """
        if file_id is None:
            file_id = self.io.generate_id()
            overwrite = True
        else:
            overwrite = False
        return self._add_document_details(file_id, self.create_body(file_path), overwrite=overwrite)

    def _add_document_details(self, file_id, body, index=AbstractElasticInterface.DEFAULT_INDEX, overwrite=True):
        """

        :param file_id:
        :param body:
        :param index:
        :param overwrite:
        :return:
        """
        print(f'Adding entry for {file_id} to {index}')

        if not overwrite:
            try:
                result = self.search_filename_by_id(file_id)
                if result is not None:
                    self.es.index(index=index, id=file_id, body=body)
                    return file_id
                else:
                    raise FileExistsError('File already exists in elasticsearch cluster')
            except FileExistsError:
                return False
        else:
            self.es.index(index=index, id=file_id, body=body)
            return file_id

    def search_filename_by_id(self, file_id, index=AbstractElasticInterface.DEFAULT_INDEX):
        """
        Search ElasticSearch for a file name using an id

        :param file_id: The id of the file to search
        :param index: ElasticSearch index to search
        :return: If file is found return the file name of the file else return None
        """

        try:
            result = self.es.search(index=index, body={"query": {"term": {'_id': file_id}}})
            if len(result[self.HITS][self.HITS]) > 1:
                raise LookupError(f'Multiple files found for id: {file_id}')

            if len(result[self.HITS][self.HITS]) == 0:
                raise LookupError(f'No files found for id: {file_id}')

            return result[self.HITS][self.HITS][0][self.SOURCE][self.DISK_LOCATION]

        except (IndexError, LookupError):
            return None

    def search_id_by_filename(self, file_name, index=AbstractElasticInterface.DEFAULT_INDEX):
        """
        Search ElasticSearch for an id using a file name

        :param file_name: The name of the file to search
        :param index: ElasticSearch index to search
        :return: If file is found return the ID of the file else return None
        """
        try:
            result = self.es.search(index=index,
                                    body={"query": {"match": {f'{self.DISK_LOCATION}.keyword': file_name}}})
            return result[self.HITS][0][self.ID]
        except KeyError:
            return None

    def show_database(self):
        """
        Show all entries in the ElasticSearch
        :return: None
        """
        return self.es.search(index=self.DEFAULT_INDEX, body={"query": {"match_all": {}}})

    def create_body(self, file_path):
        """
        Create an ElasticSearch query body
        :param file_path: The path of the file
        :return: None
        """
        return {self.DISK_LOCATION: self.io.make_server_location(file_path)}

    def populate_dummy_data(self):
        """
        Method for populating the elasticsearch server
        and adding the corresponding files to disk
        """

        # Load the dummy data
        with open('/Users/george/Projects/optibrium-devops/src/resources/dummy_data.json', 'r') as f:
            dummy_data = json.load(f)

        for key in dummy_data:
            self._add_document_details(key, dummy_data[key])
            self.io.make_dummy_file(dummy_data[key][self.DISK_LOCATION])
