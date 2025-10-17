import os
import typer
from code_tag import CodeTagEnum
from database import db, SourceCodeFile, fill_app_tables, CodeTag
from rich.table import Table
from rich.console import Console
from typing_extensions import Annotated

app = typer.Typer(no_args_is_help=True)

@app.command()
def Gather(
    project_path: Annotated[str, typer.Argument()] = os.getcwd(),
    todos: Annotated[bool, typer.Option("--todos", "-t")] = False,
    bugs: Annotated[bool, typer.Option("--bugs", "-b")] = False,
    perfs: Annotated[bool, typer.Option("--perfs", "-p")] = False,
    warns: Annotated[bool, typer.Option("--warns", "-w")] = False,
    tests: Annotated[bool, typer.Option("--tests", "-f")] = False,
    all_tags: Annotated[bool, typer.Option("--all", "-a", help="By default, only TODOs are shown. Use this flag to show all tag types")] = False
    ):
    created_project = fill_app_tables(project_path)
    table = make_display_table(created_project.name)
    row_num = 0

    tag_flag_args: list[str] = []

    if todos:
        # Yeah, it's weird to have a "--todos" option flag
        # when default behavior is to only show todos,
        # but this is how we allow for combinations like -tbf, -tpw, etc.
        tag_flag_args.append(CodeTagEnum.TODO.name)
    if bugs:
        tag_flag_args.append(CodeTagEnum.BUG.name)
    if perfs:
        tag_flag_args.append(CodeTagEnum.PERF.name)
    if warns:
        tag_flag_args.append(CodeTagEnum.WARN.name)
    if tests:
        tag_flag_args.append(CodeTagEnum.TEST.name)
    if all_tags:
        tag_flag_args = [CodeTagEnum.TODO.name, CodeTagEnum.BUG.name, CodeTagEnum.PERF.name, CodeTagEnum.WARN.name, CodeTagEnum.TEST.name]
    else:
        tag_flag_args = [CodeTagEnum.TODO.name]

    for tag in CodeTag.select().where(
        CodeTag.commit_id == created_project.commit_id,
        CodeTag.tag_name.in_(tag_flag_args)
    ):
        file_name = SourceCodeFile.get(SourceCodeFile.blob_id == tag.parent_blob_id).name
        table.add_row(
            str(row_num), 
            file_name, 
            str(tag.line_num), 
            tag.tag_name, 
            tag.message, 
            tag.commit_id, 
            tag.msg_uid
        )
        row_num += 1

    console = Console()
    console.print(table)

@app.command()
@db.connection_context()
def Print_All():
    table = make_display_table("All Tags in DB")
    row_num = 0
    for tag in CodeTag.select():
        file_name = SourceCodeFile.get(SourceCodeFile.blob_id == tag.parent_blob_id).name
        table.add_row(str(row_num), file_name, str(tag.line_num), tag.tag_name, tag.message, tag.commit_id, tag.msg_uid)
        row_num += 1

    console = Console()
    console.print(table)

# Helper functions

def make_display_table(name: str) -> Table:
    table = Table(title=name, show_lines=True)
    table.add_column("#", style="white")
    table.add_column("Filename", style="green1")
    table.add_column("Line Num", style="cyan1")
    table.add_column("Tag Type", style="magenta1")
    table.add_column("Message", style="slate_blue1")
    table.add_column("Commit ID", style="cyan1")
    table.add_column("Tag UID", style="cyan1")

    return table

if __name__ == "__main__":
    app()

