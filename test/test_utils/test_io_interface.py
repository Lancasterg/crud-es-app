from os.path import exists

import pytest
from unittest import TestCase

from werkzeug.datastructures import FileStorage

from src.utils.io_interface import InputOutputInterface


class TestInputOutputInterface(TestCase):

    def __init__(self, *args):
        super().__init__(*args)
        self.io_interface = InputOutputInterface()

    def test_generate_id(self):
        file_id = self.io_interface.generate_id()
        self.assertEqual(len(file_id), 32)

    def test_make_server_location(self):
        self.assertEqual(self.io_interface.make_server_location('testfile.test'), '/var/www/testfile.test')
        self.assertEqual(self.io_interface.make_server_location('wohoo.test'), '/var/www/wohoo.test')
        self.assertEqual(self.io_interface.make_server_location('this_is_a_test.test'), '/var/www/this_is_a_test.test')
        self.assertEqual(self.io_interface.make_server_location('/var/www/testfile.test'), '/var/www/testfile.test')

    def test_save_delete_file_short(self):
        save_file = FileStorage(filename='test_save_file.file')
        self.io_interface.save_file(save_file)
        self.assertTrue(exists('/var/www/test_save_file.file'))
        self.io_interface.delete_file('test_save_file.file')

    def test_save_delete_file_long(self):
        save_file = FileStorage(filename='/var/www/test_save_file.file')
        self.io_interface.save_file(save_file)
        self.assertTrue(exists('/var/www/test_save_file.file'))
        self.io_interface.delete_file('/var/www/test_save_file.file')
