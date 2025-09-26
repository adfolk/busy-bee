from project import Project as Prj
from code_file import CodeFile
from code_tag import CodeTag
from database import create_app_db
from peewee import Model, ForeignKeyField

db = create_app_db()

class BaseModel(Model):
    class Meta:
        database = db

class Project(BaseModel):
    def __init__(self, proj: Prj) -> None:
        self.commit_id = ForeignKeyField(proj.commit)
        self.name = proj.name

