import unittest
from cli import TagTable, TagRow
from codetag import TODO, WARNING, CodeTagInstance

todo_tag = CodeTagInstance()
todo_line = "# TODO: some stuff"
todo_tag.find_tag(todo_line, 1)

hack_tag = CodeTagInstance()
hack_line = "# HACK: some sketch shit"
hack_tag.find_tag(hack_line, 69)

warn_tag = CodeTagInstance()
warn_line = "# WARN: some more sketch shit"
warn_tag.find_tag(warn_line, 420)

bug_tag = CodeTagInstance()
bug_line = "# FIX: problems"
bug_tag.find_tag(bug_line, 9000)

project_name = "tha_carter_iv"
todo_row = TagRow(project_name, todo_tag)
hack_row = TagRow(project_name, hack_tag)
warn_row = TagRow(project_name, warn_tag)
bug_row = TagRow(project_name, bug_tag)

test_table = TagTable([todo_row, hack_row, warn_row, bug_row])

class TestTagTable(unittest.TestCase):
    def test_filter_out_tags(self):
        print(len(test_table.view))
        test_table.filter_out_tag_types(TODO, WARNING)
        print(len(test_table.view))
        for row in test_table.view:
            print(row.message)
