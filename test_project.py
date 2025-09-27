from project import Project
import unittest

python_file = '/Users/austinfolkestad/workspace/github.com/adfolk/personal-projects/busy-bee/src/simulated_src_code_files/character.py'

adventurer_todo = "Line: 1, Tag: TODO, Message: Write subclass of Adventurer to represent non-wildcard enemies."
bug_fix = "Line: 37, Tag: FIX, Message: this is a bug"
compound_todo = "Line: 54, Tag: TODO, Message: write methods to calculate compound attributes."
problem_fix = "Line: 58, Tag: FIX, Message: problem, officer?"

test_repo_path: str = "/Users/austinfolkestad/workspace/github.com/adfolk/experiments/git-monkey/"

class TestProject(unittest.TestCase):
    def test_project_integration(self):
        proj = Project(test_repo_path)
        tagged_files = proj.tagged_src_files
        for file in tagged_files:
            for tag in file.tags:
                print(tag.message)

    def test_name(self):
        proj = Project(test_repo_path)
        proj_name = proj.name
        self.assertEqual(proj_name, "git-monkey")

    def test_commit_id_length(self):
        proj = Project(test_repo_path)
        self.assertEqual(len(proj.commit_id), 40)
