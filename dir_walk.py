import os
from codetag import CodeTagInstance
from languages import SrcLangType, Lang
from parsers import extract_tagged_comments

def get_tagged_comments(abs_pathname: str) -> dict[str, list[CodeTagInstance]]:
    comment_dict = {}
    src_files = find_src_files(abs_pathname)
    for file_pathname, lang in src_files:
        tagged_comments = extract_tagged_comments(file_pathname, lang)
        if tagged_comments != None:
            comment_dict[file_pathname] = tagged_comments
    return comment_dict

def find_src_files(abs_pathname: str) -> list[tuple[str, Lang]]:
    # Return a list of all source code files in a parent directory as indicated by their file extensions

    src_files = []
    for root, dirs, files in os.walk(abs_pathname):
        if '.venv' in dirs:
            dirs.remove('.venv') # don't get todos from venv dependencies in Python projects
        for name in files:
            src_lang_type = infer_lang_type(name)
            if src_lang_type is not None:
                full_path = os.path.join(root, name)
                src_files.append((full_path, Lang(src_lang_type)))

    if src_files == []:
        NoSrcCodeFoundError = Exception("No supported source code files were found")
        raise NoSrcCodeFoundError

    return src_files

def infer_lang_type(filename: str) -> SrcLangType | None:
    for member in SrcLangType:
        if filename.endswith(member.value):
            return member
    return None

