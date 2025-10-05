import os
import os.path
import platform
import peewee as db
import tempfile
from functools import wraps

def create_app_db() -> db.Database:
    dir_path = _get_local_data_dir()
    app_dir = f"{dir_path}/busy-bee"

    if not os.path.exists(app_dir):
        os.mkdir(app_dir, mode=0o744)

    app_path = f"{app_dir}/bee_db"

    return db.SqliteDatabase(app_path, pragmas={'foreign_keys': 1})

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

