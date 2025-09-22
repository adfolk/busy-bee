from code_file import Project
from unittest import TestCase

python_file = '/Users/austinfolkestad/workspace/github.com/adfolk/personal-projects/busy-bee/src/simulated_src_code_files/character.py'

adventurer_todo = "Line: 1, Tag: TODO, Message: Write subclass of Adventurer to represent non-wildcard enemies."
bug_fix = "Line: 37, Tag: FIX, Message: this is a bug"
compound_todo = "Line: 54, Tag: TODO, Message: write methods to calculate compound attributes."
problem_fix = "Line: 58, Tag: FIX, Message: problem, officer?"

test_repo_path: str = "/home/adfolk/workspace/github.com/adfolk/experiments/monke/"

class TestProject(TestCase):
    # def test_project_tree_prop(self):
    #     proj = Project(test_repo_path)
    #     print(proj.tree)

    def test_files(self):
        proj = Project(test_repo_path)
        print(len(proj.files))
        for i in proj.files:
            print("lang:", i.lang.name_of_lang, " ; path: ", i.path)

        print(f"path: {proj.path}")


