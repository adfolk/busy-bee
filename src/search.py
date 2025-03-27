import os
from os.path import join
from languages import SrcLangType, Lang


def tag_finder(comment: str, src_lang: Lang) -> list | None:
    """Return ???.

    Placeholder
    """
    # TODO: consider merging this function with capture_comments().
    # TODO: decide how to represent code tags.
    # TODO: how to handle tag aliases (i.e. FIXME for FIX)?
    # NOTE: for each item in the list returned by capture_comments():
        # search for each type of code tag
        # when code tag is found, convert it to an object (dict, class, etc) and add it to a list
            # The code tag's data structure should preserve the following data:
                # comment message


    raise NotImplemented("Not implemented")

def capture_comments(file_string: str, src_lang: Lang) -> list[str] | None:
    """Return a list of single-line code comments.

    Comments will be searched for code tag keywords by another function.
    """
    # TODO: write pseudocode

    # NOTE: Will operate at the level of a single file. Not intended to iterate over the entire list of src_file tuples.

    raise NotImplemented("Not implemented")

def find_src_files(abs_pathname: str) -> list[tuple]:
    """Return a list of all source code files in a parent directory.
    
    List values are tuples of (abs_filepath, Lang) where:
        1. `abs_filepath` points to a file to be searched for code tags by another function
        2. `Lang` is an object containing the source language's comment operators
    """

    # WARNING: this function should always be passed an absolute pathname, or else the directory will not be reachable.

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

