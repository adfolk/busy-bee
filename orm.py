from database import create_app_db, with_app_db
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
    parent_blob_id = TextField()
    tag_name = TextField()
    message = TextField()
    line_num = IntegerField()


@with_app_db((ProjectRepo, SourceCodeFile, CodeTag))
def app_tables(path: str) -> str:
    return create_proj_tables(path)

def create_proj_tables(path: str) -> str:
    """Gets the tables to the chopper."""
    proj = Project(path)
    ProjectRepo.create(name=proj.name, commit_id=proj.commit_id, path=proj.path)
    for file in proj.tagged_src_files:
        SourceCodeFile.create(commit_id=file.commit_id, blob_id=file.blob, name=file.file_name)
        for code_tag in file.tags:
            CodeTag.create(commit_id=file.commit_id, parent_blob_id=file.blob, message=code_tag.message, line_num=code_tag.line_number, tag_name=code_tag.tag_name)
    return proj.commit_id

