from code_file import Project
from unittest import TestCase

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


