from pathlib import Path
from dir_walk import get_tagged_comments
from os import getcwd

# Logic for generating the presentation layer (basically just a md file)

# maybe a string representing the markdown elements?

def get_working_dir_name():
    this_dir = Path(getcwd())
    return this_dir.name
