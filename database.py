import os
import os.path
import platform
import sqlalchemy as db

def main():
    db_path = create_app_dir()
    engine, conn, metadata = connect_db(db_path)

    hello = db.Table('Hello', metadata,
                     db.Column('Id', db.Integer(), primary_key=True),
                     db.Column('Message', db.String(), default="Hello, world!")
                     )

    metadata.create_all(engine)

    entry = db.insert(hello).values(Id=1, Message='this is crazy')
    res = conn.execute(entry)
    output = conn.execute(hello.select()).fetchall()
    print(output)

def connect_db(db_abs_path: str) -> tuple[db.Engine, db.Connection, db.MetaData]:
    engine = db.create_engine(f"sqlite:////{db_abs_path}/tags.sqlite")
    conn = engine.connect()
    metadata = db.MetaData()
    return engine, conn, metadata

def create_app_dir() -> str:
    dir_path = get_local_data_dir()
    app_dir = f"{dir_path}/busy-bee"

    if not os.path.exists(app_dir):
        os.mkdir(app_dir, mode=0o744)

    return app_dir

def get_local_data_dir() -> str:
    data_path = os.path.expanduser("~/")
    match platform.system():
        case 'Darwin':
            data_path += "Library/Application Support"
        case 'Linux':
            data_path += ".local/share"
        case _:
            raise NotImplementedError("Only mac and linux are currently supported")

    return data_path

if __name__ == "__main__":
    main()
