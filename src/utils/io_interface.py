
from os import remove
from os.path import join, exists
from uuid import uuid4


class InputOutputInterface:
    SERVER_LOCATION = '/var/www'

    def delete_file(self, file_name):
        if exists(file_name) and self.SERVER_LOCATION in file_name:
            remove(file_name)
            print(f'{file_name} removed from file system')
        else:
            remove(join(self.SERVER_LOCATION, file_name))
            print(f'{file_name} removed from file system')

        print(f'{file_name} not found')

    def make_server_location(self, input_file_name):
        if self.SERVER_LOCATION not in input_file_name:
            return join(self.SERVER_LOCATION, input_file_name)
        else:
            return input_file_name

    def save_file(self, input_file):
        if self.SERVER_LOCATION not in input_file:
            input_file.save(join(self.SERVER_LOCATION, input_file.filename))
        else:
            input_file.save(input_file.filename)

    def generate_id(self):
        return str(uuid4()).replace('-', '')
