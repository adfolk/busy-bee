from code_file import Project
from unittest import TestCase

test_repo_path: str = "/home/adfolk/workspace/github.com/adfolk/experiments/monke/"

class TestProject(TestCase):
    def test_project_tree_prop(self):
        proj = Project(test_repo_path)
        print(proj.tree)

