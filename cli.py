import os
import typer
from typing_extensions import Annotated, Optional
from rich.table import Table
from rich.console import Console

app = typer.Typer(no_args_is_help=True)

@app.command()
def Get_Tasks(
    project_path: Annotated[str, typer.Argument()] = os.getcwd(),
    select_tag_types: Annotated[Optional[str], typer.Option(
        "--select-tags", "-s",
        help="Choose which tag types to show: [t]odo, [f]ix, [h]ack, [p]erf, [w]arning")] = None,
    ):

    global_project = os.path.basename(project_path)
    table = make_display_table(global_project)
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

def make_display_table(name: str) -> Table:
    table = Table(title=name, show_lines=True)
    table.add_column("#", style="white")
    table.add_column("Filename", style="green1")
    table.add_column("Line Num", style="cyan1")
    table.add_column("Tag Type", style="magenta1")
    table.add_column("Message", style="slate_blue1")

    return table


# def filter_arguments(tags: str) -> tuple[str]:
#     user_list = list(tags)
#     command_list = []
#     for item in user_list:
#         match item:
#             case "t":
#                 command_list.append(TODO)
#             case "f":
#                 command_list.append(FIX)
#             case "p":
#                 command_list.append(PERF)
#             case "w":
#                 command_list.append(WARNING)
#             case "h":
#                 command_list.append(HACK)
#             case _:
#                 raise ValueError(f"{item} is not an accepted argument")
#
#     return tuple(command_list)

if __name__ == "__main__":
    app()

