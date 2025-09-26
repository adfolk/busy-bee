import os
import os.path
import platform
import peewee as db

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

