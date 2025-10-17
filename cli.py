import os
import typer
from code_tag import CodeTagEnum
from database import db, fill_app_tables, CodeTag
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
    """
    Pick a root directory with a .git repo, search it for code tags, and display results. Lack of a git repo will throw an error.

    If no directory path is provided, the current working directory is chosen by default. 
    By default, only TODO tags are displayed, but this can be changed through any combination of the provided option flags.

    Please note that only committed changes will be reflected in the tag results.
    Running in a dirty repo with renames of files or directories will cause errors, but committing and rerunning should fix.
    """
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
    elif not todos and not bugs and not perfs and not warns and not tests and not all_tags:
        print("executing elif clause")
        tag_flag_args = [CodeTagEnum.TODO.name]

    for tag in CodeTag.select().where(
        CodeTag.commit_id == created_project.commit_id,
        CodeTag.tag_name.in_(tag_flag_args)
    ):
        # file_name = SourceCodeFile.get(SourceCodeFile.blob_id == tag.parent_blob_id).name
        table.add_row(
            str(row_num), 
            tag.parent_file_name, 
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
def Honey(
    todos: Annotated[bool, typer.Option("--todos", "-t")] = False,
    bugs: Annotated[bool, typer.Option("--bugs", "-b")] = False,
    perfs: Annotated[bool, typer.Option("--perfs", "-p")] = False,
    warns: Annotated[bool, typer.Option("--warns", "-w")] = False,
    tests: Annotated[bool, typer.Option("--tests", "-f")] = False,
    all_tags: Annotated[bool, typer.Option("--all", "-a", help="By default, only TODOs are shown. Use this flag to show all tag types")] = False
):
    """
    Display tags that have already been gathered.

    Can be used to avoid having to commit changes that would throw errors when running `gather`.

    Defaults to only showing TODO tags. This can be changed using the same flags that `gather` takes.
    """
    table = make_display_table("All Entries in the Busy Bee Database")
    row_num = 0
    tag_flag_args: list[str] = []
    if todos:
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
    elif not todos and not bugs and not perfs and not warns and not tests and not all_tags:
        print("executing elif clause")
        tag_flag_args = [CodeTagEnum.TODO.name]

    for tag in CodeTag.select().where(
        CodeTag.tag_name.in_(tag_flag_args)
    ):
        table.add_row(
            str(row_num), 
            tag.parent_file_name, 
            str(tag.line_num), 
            tag.tag_name, 
            tag.message, 
            tag.commit_id, 
            tag.msg_uid
        )
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

