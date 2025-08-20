import unittest
from languages import SrcLangType, Lang

class TestLangClass(unittest.TestCase):
    def test_repr_c_style(self):
        c_language = Lang(SrcLangType.CLANG)
        print(c_language)

