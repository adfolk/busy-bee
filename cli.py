import os
import typer
from typing_extensions import Annotated, Optional
from codetag import FIX, HACK, PERF, TODO, WARNING, CodeTagInstance
from dir_walk import get_tagged_comments
from rich.table import Table
from rich.console import Console

app = typer.Typer(no_args_is_help=True)

@app.command()
def Task_Table(
    project_path: Annotated[str, typer.Argument()] = os.getcwd(),
    select_tag_types: Annotated[Optional[str], typer.Option(
        "--select-tags", "-s",
        help="Choose which tag types to show: [t]odo, [f]ix, [h]ack, [p]erf, [w]arning")] = None,
    ):
    name_of_project = os.path.basename(project_path)
    todo_result = get_tagged_comments(project_path)

    table = Table(title=name_of_project, show_lines=True)
    table.add_column("#", style="white")
    table.add_column("Filename", style="green1")
    table.add_column("Line Num", style="cyan1")
    table.add_column("Tag Type", style="magenta1")
    table.add_column("Message", style="slate_blue1")

    tag_table = TagTable()
    for pathname in todo_result:
        tag_list = todo_result[pathname]
        file_name = os.path.basename(pathname)

        for todo_item in tag_list:
            new_row = TagRow(file_name, todo_item)
            tag_table.add_tag(new_row)

    match select_tag_types:
        case None:
            tag_table.filter_for_tag_type(TODO, FIX, PERF, HACK, WARNING)
        case _:
            tag_table.filter_for_tag_type(*filter_arguments(select_tag_types))

    i = 0
    for row in tag_table.view:
        table.add_row(
            str(i),
            row.file_name,
            row.line_num,
            row.tag_name,
            row.message
        )
        i += 1

    console = Console()
    console.print(table)

def filter_arguments(tags: str) -> tuple[str]:
    user_list = list(tags)
    command_list = []
    for item in user_list:
        match item:
            case "t":
                command_list.append(TODO)
            case "f":
                command_list.append(FIX)
            case "p":
                command_list.append(PERF)
            case "w":
                command_list.append(WARNING)
            case "h":
                command_list.append(HACK)
            case _:
                raise ValueError(f"{item} is not an accepted argument")

    return tuple(command_list)

class TagRow:
    def __init__(self, file_name: str, tag: CodeTagInstance):
        self.file_name = file_name
        self.line_num = str(tag.line_number)
        self.tag_name = tag.tag_name
        self.message = tag.message

class TagTable:
    def __init__(self, tag_list: list[TagRow]=[]):
        self._tags = tag_list
        self.view = tag_list

    def add_tag(self, tag: TagRow):
        self._tags.append(tag)

    def filename_sort(self):
        self.view = sorted(self.view, key=lambda tag: tag.file_name)

    def tag_name_sort(self):
        self.view = sorted(self.view, key=lambda tag: tag.tag_name)

    def filter_for_tag_type(self, *tag_type: str):
        filtered = []
        selected = {*tag_type}

        for tag in self.view:
            if tag.tag_name in selected:
                filtered.append(tag)

        self.view = filtered

    def hide_entries(self, *row_nums: int):
        chopping_block = []
        for i in row_nums:
            try:
                chopping_block.append(self.view[i])
            except IndexError:
                print(f"Error: row number {i} does not exist")

        for tag in chopping_block:
            self.view.remove(tag)

    def reset_view(self):
        self.view = self._tags

if __name__ == "__main__":
    app()
