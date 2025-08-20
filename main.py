import os
import typer
from dir_walk import get_tagged_comments
from rich.pretty import pprint
from rich.table import Table
from rich.console import Console

app = typer.Typer(no_args_is_help=True)

@app.command()
def main():
    print("Hello from busy-bee!")

@app.command()
def todos():
    target = os.getcwd()
    todo_result = get_tagged_comments(target)
    for pathname in todo_result:
        cur_list = todo_result[pathname]
        for tag_item in cur_list:
            pprint(tag_item.message)

if __name__ == "__main__":
    app()
