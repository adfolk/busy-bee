import os
from languages import SrcLangType, Lang
from parsers import extract_todo

def parse_src_files(abs_pathname: str) -> list:
    src_files = find_src_files(abs_pathname)
    comments = []
    todos = []
    for name, lang in src_files:
        cm_ln, td_itm = extract_todo(name, lang)
        comments.extend(cm_ln)
        todos.extend(td_itm)
    return comments, todos

def find_src_files(abs_pathname: str) -> list[tuple]:
    """Return a list of all source code files in a parent directory as indicated by their file extensions."""

    src_files = []
    for root, dirs, files, rootfd in os.fwalk(abs_pathname):
        for name in files:
            src_lang_type = infer_lang_type(name)
            if src_lang_type is not None:
                full_name = os.path.join(root, name)
                src_files.append((full_name, Lang(src_lang_type)))

    if src_files == []:
        NoSrcCodeFoundError = Exception("No supported source code files were found")
        raise NoSrcCodeFoundError

    return src_files

def infer_lang_type(filename: str) -> SrcLangType | None:
    for member in SrcLangType:
        if filename.endswith(member.value):
            return member
    return None

