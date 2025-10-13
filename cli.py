import os
import typer
from database import app_tables, CodeTag
from rich.table import Table
from rich.console import Console
from typing_extensions import Annotated

app = typer.Typer(no_args_is_help=True)

@app.command()
def Get_Tasks(
    project_path: Annotated[str, typer.Argument()] = os.getcwd(),
    all_tag_types: Annotated[bool, typer.Option("--all", "-a", help="Show all tag types")] = False,
    ):
    created_project = app_tables(project_path)

    # TODO: avoid creating duplicate records upon rerunning command on same directory

    # HACK: this entire project

    table = make_display_table(created_project.name)

    match all_tag_types:
        case False:
            for tag in CodeTag.select().where(CodeTag.commit_id == created_project.commit_id, CodeTag.tag_name == "TODO"):
                table.add_row('0', tag.parent_blob_id, str(tag.line_num), tag.tag_name, tag.message, tag.commit_id, tag.msg_uid)
        case True:
            for tag in CodeTag.select().where(CodeTag.commit_id == created_project.commit_id):
                table.add_row('0', tag.parent_blob_id, str(tag.line_num), tag.tag_name, tag.message, tag.commit_id, tag.msg_uid)

    console = Console()
    console.print(table)

@app.command()
def Hide_Entries(
    tag_ids: Annotated[list[str], typer.Argument()]
    ):
    """
    Pass in a string of numbers delimited by whitespace.

    Example: 1 3 8 10
    """
    raise NotImplementedError("not done yet")


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

