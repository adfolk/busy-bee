from database import create_app_db
from project import Project
from peewee import IntegerField, Model, TextField

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
    tag_name = TextField()
    message = TextField()
    line_num = IntegerField()

