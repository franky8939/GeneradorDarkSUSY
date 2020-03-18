from unittest import TestCase
from modules.all.modification_files import file_clear, file_exists
import os

directory = 'temp_test'
file_name = 'test_file.txt'


class Test(TestCase):
    # def test_file_clear(self):
    #     self.assertFalse(file_clear(os.path.join(directory, file_name), mode='f'))
    # self.assertTrue(file_clear(os.path.join(directory, file_name), mode='f'))

    def test_file_clear_inputs(self):
        self.assertRaises(TypeError, file_clear, os.path.join(directory, file_name), mode=5)
        self.assertRaises(TypeError, file_clear, os.path.join(directory, file_name), mode='k')
        self.assertRaises(TypeError, file_clear, os.path.join(directory, file_name), mode=5j)
        self.assertRaises(TypeError, file_clear, os.path.join(directory, file_name), mode=1.0)

    def test_file_exists_inputs(self):
        self.assertRaises(TypeError, file_exists, 5)
        self.assertRaises(TypeError, file_exists, 5j)
        self.assertRaises(TypeError, file_exists, 5.0)
