import os
import typer
from database import SourceCodeFile, app_tables, CodeTag
from rich.table import Table
from rich.console import Console
from typing_extensions import Annotated

app = typer.Typer(no_args_is_help=True)

@app.command()
def Get_Tasks(
    project_path: Annotated[str, typer.Argument()] = os.getcwd(),
    all_tag_types: Annotated[bool, typer.Option("--all", "-a", help="Show all tag types")] = False
    ):
    created_project = app_tables(project_path)

    # TODO: avoid creating duplicate records upon rerunning command on same directory

    table = make_display_table(created_project.name)

    row_num = 0

    if all_tag_types == False:
        for tag in CodeTag.select().where(CodeTag.commit_id == created_project.commit_id, CodeTag.tag_name == "TODO"):
            file_name = SourceCodeFile.get(SourceCodeFile.blob_id == tag.parent_blob_id).name
            table.add_row(str(row_num), file_name, str(tag.line_num), tag.tag_name, tag.message, tag.commit_id, tag.msg_uid)
            row_num += 1
    else:
        for tag in CodeTag.select().where(CodeTag.commit_id == created_project.commit_id):
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

