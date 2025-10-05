from database import create_app_db
from project import Project
from peewee import ForeignKeyField, IntegerField, Model, TextField

database = create_app_db()

class BaseModel(Model):
    class Meta:
        database = database

class ProjectRepo(BaseModel):
    commit_id = TextField()
    name = TextField()
    path = TextField()

class SourceCodeFile(BaseModel):
    commit_id = ForeignKeyField(ProjectRepo, backref='commit_id')
    blob_id = TextField()
    name = TextField()

class CodeTag(BaseModel):
    # commit_id = ForeignKeyField(ProjectRepo, backref='commit_id')
    parent_blob_id = ForeignKeyField(SourceCodeFile, backref='blob_id')
    tag_name = TextField()
    message = TextField()
    line_num = IntegerField()


def create_db_with_project_files(path_name: str):
    db = database
    db.connect()
    db.create_tables([ProjectRepo, SourceCodeFile, CodeTag])

    proj = Project(path_name)
    src_files = proj.src_files
    tagged_files = proj.tagged_src_files
<<<<<<< HEAD
    print(proj.commit_id)
    rpo = ProjectRepo(name=proj.name, commit_id=proj.commit_id, path=proj.path)
    print(rpo.commit_id)
    rpo.save()
    print(f"\n*****************\nSUCCESS - created ProjectRepo with commit hash {ProjectRepo.commit_id}\nfrom Project commit hash: {proj.commit_id}\n***************************\n")
    for file in src_files:
        SourceCodeFile.create(
            commit_id = file.commit_id,
=======
    ProjectRepo.create(
        commit_id = proj.commit_id,
        name = proj.name,
        path = proj.path
    )
    for file in src_files:
        SourceCodeFile.create(
            commit_id = proj.commit_id,
>>>>>>> 2ebfc25 (db test runner)
            blob_id = file.blob,
            name = file.file_name
        )
    for file in tagged_files:
        for tag in file.tags:
            CodeTag.create(
<<<<<<< HEAD
=======
                commit_id = proj.commit_id,
>>>>>>> 2ebfc25 (db test runner)
                parent_blob_id = tag.blob_parent,
                tag_name = tag.tag_name,
                message = tag.message,
                line_num = tag.line_number
            )

    db.close()


