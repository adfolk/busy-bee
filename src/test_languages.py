import unittest
from languages import SrcLangType, Lang

class TestLang(unittest.TestCase):
    def test_repr_c_style(self):
        c_language = Lang(SrcLangType.CLANG_SRC)
        print(c_language)

