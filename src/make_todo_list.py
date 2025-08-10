from codetag import CodeTagInstance
from pathlib import Path
from os import getcwd

# Logic for generating the presentation layer (basically just a md file)

def set_working_dir_name():
    this_dir = Path(getcwd())
    return f"# {this_dir.name}"

def unpack_tag_lists(tag_dict: dict):
    giant_list_str = ""
    for key, value in tag_dict:
        todos = organize_by_tag_type(value)
        file_entry = f"## {key}\n\n{todos}"
        giant_list_str += file_entry

    return giant_list_str

def organize_by_tag_type(tags: list[CodeTagInstance]):
    todos = ""
    fixmes = ""
    perfs = ""

    for item in tags:
        match item.tag_name:
            case "TODO":
                todos += f"- [  ] {item.message}\n"
            case "FIX":
                fixmes += f"- [  ] {item.message}\n"
            case "PERF":
                perfs += f"- [  ] {item.message}\n"

    return f"### TODO\n{todos}\n### FIXME\n{fixmes}\n### OPTIMIZE\n{perfs}\n\n"

