import unittest
from search import find_src_files

class TestFileParsing(unittest.TestCase):
    def test_find_src_files(self):
        target_dir = 'simulated_src_code_files/'
        print(find_src_files(target_dir))

