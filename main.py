import os
import typer
from typing_extensions import Annotated
from dir_walk import get_tagged_comments
from rich.pretty import pprint
from rich.table import Table
from rich.console import Console

app = typer.Typer(no_args_is_help=True)

@app.command()
def main():
    print("Hello from busy-bee!")

@app.command()
def Todo_Flat_List():
    target = os.getcwd()
    todo_result = get_tagged_comments(target)
    for pathname in todo_result:
        cur_list = todo_result[pathname]
        for tag_item in cur_list:
            pprint(tag_item.message)

@app.command()
def Show_Todo_Table(project_path: Annotated[str, typer.Argument()] = os.getcwd()):
    name_of_project = os.path.basename(project_path)
    todo_result = get_tagged_comments(project_path)

    table = Table(title=name_of_project)
    table.add_column("Filename", style="green1")
    table.add_column("Line Num", style="cyan1")
    table.add_column("Tag Type", style="magenta1")
    table.add_column("Message", style="slate_blue1")

    for pathname in todo_result:
        tag_list = todo_result[pathname]
        for todo_item in tag_list:
            table.add_row(
                os.path.basename(pathname),
                str(todo_item.line_number),
                todo_item.tag_name,
                todo_item.message
            )

    console = Console()
    console.print(table)


if __name__ == "__main__":
    app()
