import os
from os.path import join
from languages import SrcLangType

# Steps:
    # Iterate through files recursively
    # If file extension matches a supported language enum (see languages.py module), add it to a list with the SrcLangType enum member.
    # Read in each file.
    # Regex capture each comment. If comment contains TODO keyword, add comment to list.

def find_src_files(abs_pathname: str) -> list:

    # WARNING: this function should always be passed an absolute pathname, or else the directory will not be reachable.

    src_files = []
    for root, dirs, files, rootfd in os.fwalk(abs_pathname):
        for name in files:
            src_lang_type = infer_lang_type(name)
            if src_lang_type is not None:
                full_name = os.path.join(root, name)
                src_files.append((full_name, src_lang_type))

    if src_files == []:
        NoSrcCodeFoundError = Exception("No supported source code files were found")
        raise NoSrcCodeFoundError

    return src_files

def infer_lang_type(filename: str):
    for member in SrcLangType:
        if filename.endswith(member.value):
            return member
    return None

