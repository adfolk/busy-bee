from database import create_app_db
from project import Project
from peewee import CharField, IntegerField, Model, ForeignKeyField, TextField

database = create_app_db()

def get_project_files_and_create(path_name: str):
    db = database
    db.connect()
    db.create_tables([ProjectRepo, SourceCodeFile, CodeTag])

    proj = Project(path_name)
    src_files = proj.src_files
    tagged_files = proj.tagged_src_files
    proj_orm = ProjectRepo.create(
        commit_id = proj.commit_id,
        name = proj.name,
        path = proj.path
    )
    for file in src_files:
        src_f_orm = SourceCodeFile.create(
            commit_id = proj.commit_id,
            blob_id = file.blob,
            name = file.file_name
        )
    for file in tagged_files:
        for tag in file.tags:
            tag_orm = CodeTag.create(
                commit_id = proj.commit_id,
                parent_blob_id = tag.blob_parent,
                tag_name = tag.tag_name,
                message = tag.message,
                line_num = tag.line_number
            )

    db.close()

class BaseModel(Model):
    class Meta:
        database = database

class ProjectRepo(BaseModel):
    commit_id = CharField(max_length=40)
    name = TextField()
    path = TextField()

class SourceCodeFile(BaseModel):
    commit_id = ForeignKeyField(ProjectRepo, backref='commit_id')
    blob_id = CharField(max_length=40)
    name = TextField()

class CodeTag(BaseModel):
    commit_id = ForeignKeyField(ProjectRepo, backref='commit_id')
    parent_blob_id = ForeignKeyField(SourceCodeFile, backref='blob_id')
    tag_name = TextField()
    message = TextField()
    line_num = IntegerField()

