import os
import typer
from typing_extensions import Annotated
from codetag import CodeTagInstance
from dir_walk import get_tagged_comments
from rich.table import Table
from rich.console import Console

app = typer.Typer(no_args_is_help=True)

@app.command()
def Task_Table(
    project_path: Annotated[str, typer.Argument()] = os.getcwd(),
    all_tags: Annotated[bool, typer.Option(help="Include all types of code tags in the table")] = False,
               ):
    # TODO: test sort and filter methods
    # TODO: define option flags
    # TODO: each table row different color based on module name
    # TODO: write docstring
    name_of_project = os.path.basename(project_path)
    todo_result = get_tagged_comments(project_path)

    table = Table(title=name_of_project, show_lines=True)
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

    # handle flags
    tag_table.filename_sort()
    processed_tags = tag_table.tags
    if not all_tags:
        processed_tags = tag_table.tag_name_filter("TODO")

    for row in processed_tags:
        table.add_row(
            row.file_name,
            row.line_num,
            row.tag_name,
            row.message
        )

    console = Console()
    console.print(table)

# Helper functions for app commands

class TagRow:
    def __init__(self, file_name: str, tag: CodeTagInstance):
        self.file_name = file_name
        self.line_num = str(tag.line_number)
        self.tag_name = tag.tag_name
        self.message = tag.message

class TagTable:
    def __init__(self, tag_list: list[TagRow]=[]):
        self.tags = tag_list

    def add_tag(self, tag: TagRow):
        self.tags.append(tag)

    def filename_sort(self):
        self.tags = sorted(self.tags, key=lambda tag: tag.file_name)

    def tag_name_sort(self):
        self.tags = sorted(self.tags, key=lambda tag: tag.tag_name)

    def tag_name_filter(self, tag_type: str) -> list[TagRow] | list:
        filtered = []
        for tag in self.tags:
            if tag.tag_name == tag_type:
                filtered.append(tag)
        return filtered


if __name__ == "__main__":
    app()
