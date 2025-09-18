import os
from codetag import CodeTagInstance
from code_file import SrcLangType, Lang, CodeFile
from parsers import extract_tagged_comments

def get_tagged_comments(abs_pathname: str) -> dict[str, list[CodeTagInstance]]:
    comment_dict = {}
    src_files = find_src_files(abs_pathname)
    for file_pathname, lang in src_files:
        tagged_comments = extract_tagged_comments(file_pathname, lang)
        if tagged_comments != None:
            comment_dict[file_pathname] = tagged_comments
    return comment_dict

def get_src_files(project_path: str) -> list[CodeFile]:
    # will replace find_src_files
    src_files = []
    for root, dirs, files in os.walk(project_path):
        if '.venv' in dirs:
            dirs.remove('.venv') # don't get todos from Python virtual environments
            # TODO: research other cases of things to avoid searching
        for name in files:
            src_lang_type = infer_lang_type(name)
            if src_lang_type is not None:
                # TODO: test whether this handles multiple levels in dir structures
                full_path = os.path.join(root, name)
                new_entry = CodeFile(project_path, full_path, src_lang_type)
                src_files.append(new_entry)
    if src_files == []:
        NoSrcCodeFoundError = Exception("No supported source code files were found")
        raise NoSrcCodeFoundError

    return src_files

def find_src_files(abs_pathname: str) -> list[tuple[str, Lang]]:
    # Return a list of all source code files in a parent directory as indicated by their file extensions

    src_files = []
    for root, dirs, files in os.walk(abs_pathname):
        if '.venv' in dirs:
            dirs.remove('.venv') # don't get todos from Python virtual environments
            # TODO: research other cases of things to avoid searching
        for name in files:
            src_lang_type = infer_lang_type(name)
            if src_lang_type is not None:
                # TODO: test whether this handles multiple levels in dir structures
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

