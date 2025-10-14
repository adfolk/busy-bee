import os
import os.path
import platform
import tempfile
from functools import wraps
from project import Project
from peewee import Database, IntegrityError, SqliteDatabase, IntegerField, Model, TextField

def create_app_db() -> Database:
    dir_path = _get_local_data_dir()
    app_dir = f"{dir_path}/busy-bee"

    if not os.path.exists(app_dir):
        os.mkdir(app_dir, mode=0o744)

    app_path = f"{app_dir}/bee_db"

    return SqliteDatabase(app_path)

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

db = create_app_db()

class BaseModel(Model):
    class Meta:
        database = db

class ProjectRepo(BaseModel):
    commit_id = TextField(primary_key=True)
    name = TextField()
    path = TextField()

class SourceCodeFile(BaseModel):
    commit_id = TextField()
    blob_id = TextField()
    name = TextField()

class CodeTag(BaseModel):
    commit_id = TextField()
    parent_blob_id = TextField()
    msg_uid = TextField()
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
                app_db.close()
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
            test_db = SqliteDatabase(os.path.join(tempfile.gettempdir(), 'test_bee.db'))
            with test_db.bind_ctx(dbs):
                test_db.create_tables(dbs)
                try:
                    func(*args, **kwargs)
                finally:
                    test_db.drop_tables(dbs)
                    test_db.close()
        return test_db_closure
    return decorator

@db.connection_context()
def app_tables(path: str) -> Project:
    db.create_tables([ProjectRepo, SourceCodeFile, CodeTag])
    return create_proj_tables(path)

def create_proj_tables(path: str) -> Project:
    """Gets the tables to the chopper."""
    proj = Project(path)
    if proj.repo.is_dirty():
        print("Running from dirty repo will not capture tags in untracked or uncommitted files")
    try:
        ProjectRepo.create(name=proj.name, commit_id=proj.commit_id, path=proj.path)
        for file in proj.tagged_src_files:
            try:
                SourceCodeFile.create(commit_id=file.commit_id, blob_id=file.blob, name=file.file_name)
                for code_tag in file.tags:
                    try:
                        CodeTag.create(commit_id=file.commit_id, parent_blob_id=file.blob, msg_uid=code_tag.digest, message=code_tag.message, line_num=code_tag.line_number, tag_name=code_tag.tag_name)
                    except IntegrityError:
                        continue
            except IntegrityError:
                continue
    except IntegrityError:
        print(f"Project {proj.name} with commit ID {proj.commit_id} already exists")
    return proj

