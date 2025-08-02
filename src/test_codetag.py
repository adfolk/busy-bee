import unittest
from codetag import CodeTagInstance

todo_line = "# TODO: write test for this"
fix_alt_BUG = "# BUG: this is broken"
alt_perf = "# OPTIM: make this faster"
warn_line = "# WARNING: this hard-coded global var is depended on by the entire program lol"

class TestTagType(unittest.TestCase):
    def test_codetag_aliasing(self):
        tag_type_obj = CodeTagInstance()
        tag_t = tag_type_obj.find_tag(fix_alt_BUG, 1)
        fix = "FIX"
        msg = "this is broken"
        self.assertEqual(tag_t, True)
        self.assertEqual(tag_type_obj.message, msg)
        self.assertEqual(tag_type_obj.tag_name, fix)
