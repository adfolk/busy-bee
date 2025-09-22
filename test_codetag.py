import unittest
from codetag import CodeTag

todo_line = "# TODO: write test for this"
fix_alt_BUG = "# BUG: this is broken"
alt_perf = "# OPTIM: make this faster"
warn_line = "# WARNING: this hard-coded global var is depended on by the entire program lol"

class TestTagType(unittest.TestCase):
    def test_codetag_matching(self):
        text = "BUG"
        tag = CodeTag.which_tag(text)
        self.assertEqual(tag, CodeTag.BUG)

