from os import remove
from os.path import join, exists
from uuid import uuid4


class InputOutputInterface:
    SERVER_LOCATION = '/var/www'

    def delete_file(self, file_name: str) -> None:
        """
        Delete a file from the file system
        :param file_name: The name of the file to be deleted
        :return: None
        """
        file_name = self.make_server_location(file_name)
        if exists(file_name):
            remove(file_name)
            print(f'{file_name} removed from file system')
        else:
            raise FileNotFoundError('File not found on filesystem')

    def make_server_location(self, input_file_name: str) -> str:
        """
        Make sure that we only upload files to /var/www
        :param input_file_name: The name of the file to upload
        :return: str like: /var/www/filename.txt
        """
        if self.SERVER_LOCATION not in input_file_name:
            return join(self.SERVER_LOCATION, input_file_name)
        else:
            return input_file_name

    def save_file(self, input_file) -> None:
        """
        Save an input file to /www/var
        :param input_file: The name of the file to save
        :return: None
        """
        input_file.save(self.make_server_location(input_file.filename))

    def generate_id(self) -> str:
        """
        Generate a unique id of length 32
        :return: Unique id of length 32
        """
        return str(uuid4()).replace('-', '')
