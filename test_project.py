from project import Project
import unittest

test_repo_path: str = "/home/adfolk/workspace/github.com/adfolk/experiments/monke/"

proj = Project(test_repo_path)

class TestProject(unittest.TestCase):
    def test_project_integration(self):
        tagged_files = proj.tagged_src_files
        for file in tagged_files:
            for tag in file.tags:
                print(tag.message)

    def test_name(self):
        proj_name = proj.name
        self.assertEqual(proj_name, "monke")

    def test_commit_id_length(self):
        self.assertEqual(len(proj.commit_id), 40)

    def test_proj_has_files(self):
        tag_files = proj.tagged_src_files
        print(tag_files)
