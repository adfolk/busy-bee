import unittest
from code_tag import CodeTagEnum

todo_line = "# TODO: write test for this"
fix_alt_BUG = "# BUG: this is broken"
alt_perf = "# OPTIM: make this faster"
warn_line = "# WARNING: this hard-coded global var is depended on by the entire program lol"

class TestTagType(unittest.TestCase):
    def test_codetag_matching(self):
        text = "BUG"
        tag = CodeTagEnum.which_tag(text)
        self.assertEqual(tag, CodeTagEnum.BUG)

        other_text = "TODO"
        other_tag = CodeTagEnum.which_tag(other_text)
        self.assertEqual(other_tag, CodeTagEnum.TODO)

