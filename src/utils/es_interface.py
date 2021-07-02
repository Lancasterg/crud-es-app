from typing import Dict

from elasticsearch import Elasticsearch
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


class ElasticInterface(AbstractElasticInterface):

    def __init__(self, host='elastic', port=9200):
        self.es = Elasticsearch([{'host': host, 'port': port}])

        # If we haven't yet instantiated the file_index, do so now
        if not self.es.indices.exists(index="file_index"):
            self.es.indices.create(index='file_index')

        self.io = InputOutputInterface()
        self._log = get_default_logger(__class__.__name__)

    def delete_file_by_id(self, file_id: str) -> str:
        """
        Given a file id, delete the id from ElasticSearch
        :param file_id: The file id to delete
        :return: The name of the deleted file
        """
        file_name = self.search_filename_by_id(file_id)
        if file_name is None:
            raise FileNotFoundError('File not found in elasticsearch index.')
        elif file_name is not None:
            self.es.delete(index=self.DEFAULT_INDEX, id=file_id)
        return file_name

    def add_document_details(self, file_path: str, file_id: str = None) -> str:
        """
        Public wrapper method for _add_document_details

        :param file_path: The path of the file to be added to ElasticSearch
        :param file_id: The id of the file to be added to ElasticSearch. If none, we generate a new id.
        :return: file_id
        """
        if file_id is None:
            file_id = self.io.generate_id()
        return self._add_document_details(file_id, self.create_body(file_path))

    def _add_document_details(self, file_id: str, body: Dict,
                              index: str = AbstractElasticInterface.DEFAULT_INDEX) -> str:
        """
        :param file_id: The id of the file to be added to ElasticSearch
        :param body: The body of the request to ElasticSearch
        :param index: The index of ElasticSearch to add our data to
        :return: file_id
        """
        print(f'Adding entry for {file_id} to {index}')
        self.es.index(index=index, id=file_id, body=body)
        return file_id

    def search_filename_by_id(self, file_id: str, index=AbstractElasticInterface.DEFAULT_INDEX) -> str:
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

        except LookupError:
            return None

    def search_id_by_filename(self, file_name: str, index=AbstractElasticInterface.DEFAULT_INDEX):
        """
        Search ElasticSearch for an id using a file name

        :param file_name: The name of the file to search
        :param index: ElasticSearch index to search
        :return: If file is found return the ID of the file else return None
        """
        try:
            file_name = self.io.make_server_location(file_name)
            result = self.es.search(index=index,
                                    body={"query": {"match": {f'{self.DISK_LOCATION}.keyword': file_name}}})
            file_id = result[self.HITS][self.HITS][0][self.ID]
            return file_id
        except IndexError:
            return None

    def show_database(self) -> Dict:
        """
        Show all entries in the ElasticSearch
        :return: None
        """
        return self.es.search(index=self.DEFAULT_INDEX, body={"query": {"match_all": {}}})

    def create_body(self, file_path: str) -> Dict:
        """
        Create an ElasticSearch query body
        :param file_path: The path of the file
        :return: None
        """
        return {self.DISK_LOCATION: self.io.make_server_location(file_path)}


class MockElasticInterface(AbstractElasticInterface):
    """
    Mock class for unit testing without spinning up an ES cluster
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
            return self.fake_es.pop(file_id)
        except KeyError:
            return None
