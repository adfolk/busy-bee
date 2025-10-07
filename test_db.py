import os
from database import app_tables, with_test_db, _get_local_data_dir, create_proj_tables, ProjectRepo, SourceCodeFile, CodeTag
import unittest
import git
from project import Project

tppath = "/Users/austinfolkestad/workspace/github.com/adfolk/experiments/git-monkey/"

class TestAppDb(unittest.TestCase):
    def test_proj(self):
        lcl_proj = Project(tppath)
        self.assertEqual(lcl_proj.commit_id, "d6a57df5351ce817e16eec8e4586ebb4e94c8302")

    def test_app_db_creation(self):
        app_tables(tppath)
        prj = ProjectRepo.get(ProjectRepo.commit_id == 'd6a57df5351ce817e16eec8e4586ebb4e94c8302')
        a = prj.commit_id
        self.assertEqual(a, git.Repo(tppath).head.commit.hexsha)

    def test_app_db_exists(self):
        db_path = f"{_get_local_data_dir()}/busy-bee/bee_db"
        self.assertTrue(os.path.exists(db_path))

    def test_test_db(self):
        @with_test_db((ProjectRepo, SourceCodeFile, CodeTag))
        def query_all(path: str):
            cmt = create_proj_tables(path)
            print(cmt)
            for tag in CodeTag.select():
                print(f"type: {tag.tag_name}\nmessage: {tag.message}")
        query_all(tppath)

