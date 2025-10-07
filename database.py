import os
import os.path
import platform
import peewee as db
import tempfile
from functools import wraps
from project import Project
from peewee import IntegerField, Model, TextField

def create_app_db() -> db.Database:
    dir_path = _get_local_data_dir()
    app_dir = f"{dir_path}/busy-bee"

    if not os.path.exists(app_dir):
        os.mkdir(app_dir, mode=0o744)

    app_path = f"{app_dir}/bee_db"

    return db.SqliteDatabase(app_path)

def _get_local_data_dir() -> str:
    data_path = os.path.expanduser("~/")
    match platform.system():
        case 'Darwin':
            data_path += "Library/Application Support"
        case 'Linux':
            data_path += ".local/share"
        case _:
            raise NotImplementedError("Only mac and linux are currently supported")

    return data_path

database = create_app_db()

class BaseModel(Model):
    class Meta:
        database = database

class ProjectRepo(BaseModel):
    commit_id = TextField()
    name = TextField()
    path = TextField()

class SourceCodeFile(BaseModel):
    commit_id = TextField()
    blob_id = TextField()
    name = TextField()

class CodeTag(BaseModel):
    commit_id = TextField()
    parent_blob_id = TextField()
    tag_name = TextField()
    message = TextField()
    line_num = IntegerField()




def with_app_db(dbs: tuple):
    """Decorator for managing the application's database connection."""
    def decorator(func):
        @wraps(func)
        def app_db_closure(*args, **kwargs):
            app_db = create_app_db()
            with app_db.bind_ctx(dbs):
                app_db.create_tables(dbs)
                func(*args, **kwargs)
        return app_db_closure
    return decorator

def with_test_db(dbs: tuple):
    """
    Create a test db in memory and bind it to the ORM models.
    This creates the tables, runs the test function, and then drops the tables.

    :param dbs: A tuple of the models to bind to the test database.
    
    Adapted from this blog post: https://medium.com/@aaronfulton/mocking-with-peewee-pytest-a84442bfbb77
    """
    def decorator(func):
        @wraps(func)
        def test_db_closure(*args, **kwargs):
            test_db = db.SqliteDatabase(os.path.join(tempfile.gettempdir(), 'test_bee.db'))
            with test_db.bind_ctx(dbs):
                test_db.create_tables(dbs)
                try:
                    func(*args, **kwargs)
                finally:
                    test_db.drop_tables(dbs)
                    test_db.close()
        return test_db_closure
    return decorator

@with_app_db((ProjectRepo, SourceCodeFile, CodeTag))
def app_tables(path: str) -> None:
    create_proj_tables(path)

def create_proj_tables(path: str) -> None:
    """Gets the tables to the chopper."""
    proj = Project(path)
    ProjectRepo.create(name=proj.name, commit_id=proj.commit_id, path=proj.path)
    for file in proj.tagged_src_files:
        SourceCodeFile.create(commit_id=file.commit_id, blob_id=file.blob, name=file.file_name)
        for code_tag in file.tags:
            CodeTag.create(commit_id=file.commit_id, parent_blob_id=file.blob, message=code_tag.message, line_num=code_tag.line_number, tag_name=code_tag.tag_name)
    # return proj.commit_id
