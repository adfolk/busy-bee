from codetag import CodeTagInstance

# Logic for generating the presentation layer (basically just a md file)

def compose_tag_doc(tag_dict: dict) -> str:
    """Iterate through all tags found in a given root directory by get_tagged_comments() and put them into a md string."""
    giant_list_str = ""
    for key, value in tag_dict:
        todos = organize_by_tag_type(value)
        file_entry = f"## {key}\n\n{todos}"
        giant_list_str += file_entry

    return giant_list_str

def organize_by_tag_type(tags: list[CodeTagInstance]) -> str:
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

