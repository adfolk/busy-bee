from database import create_app_db
from peewee import CharField, IntegerField, Model, ForeignKeyField, TextField

db = create_app_db()

class BaseModel(Model):
    class Meta:
        database = db

class Project(BaseModel):
    commit_id = CharField(max_length=40)
    name = TextField()
    path = TextField()

class SourceCodeFile(BaseModel):
    commit_id = ForeignKeyField(Project, backref='commit_id')
    blob_id = CharField(max_length=40)
    name = TextField()

class CodeTag(BaseModel):
    commit_id = ForeignKeyField(Project, backref='commit_id')
    parent_blob_id = ForeignKeyField(SourceCodeFile, backref='blob_id')
    tag_name = TextField()
    message = TextField()
    line_num = IntegerField()

