import unittest
from languages import Lang, SrcLangType
from parsers import extract_tagged_comments

python_file = '/Users/austinfolkestad/workspace/github.com/adfolk/personal-projects/busy-bee/src/simulated_src_code_files/character.py'

adventurer_todo = "Line: 1, Tag: TODO, Message: Write subclass of Adventurer to represent non-wildcard enemies."
bug_fix = "Line: 37, Tag: FIX, Message: this is a bug"
compound_todo = "Line: 54, Tag: TODO, Message: write methods to calculate compound attributes."
problem_fix = "Line: 58, Tag: FIX, Message: problem, officer?"


class TestTagExtract(unittest.TestCase):
    def test_py_extract(self):
        pylang = Lang(SrcLangType.PYTHON)
        text_of_comments = []
        comments = extract_tagged_comments(python_file, pylang)
        for item in comments:
            txt_string = str(item)
            text_of_comments.append(txt_string)

        self.assertIn(adventurer_todo, text_of_comments)
        self.assertIn(bug_fix, text_of_comments)
        self.assertIn(compound_todo, text_of_comments)
        self.assertIn(problem_fix, text_of_comments)

