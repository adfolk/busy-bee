from io import TextIOWrapper
from typing import Generator
from languages import Lang
from codetag import CodeTagInstance


def extract_tagged_comments(file_pathname: str, lang: Lang) -> list[CodeTagInstance] | None:
    with open(file_pathname) as f:
        tag_list = []
        current_tag = CodeTagInstance()
        for num_ln, comment in iterate_comments(f, lang):
            has_code_tag = current_tag.find_tag(comment, num_ln)
            if has_code_tag == True:
                tag_list.append(current_tag)
                current_tag = CodeTagInstance()
        if tag_list != []:
            return tag_list
        return None

def iterate_comments(file: TextIOWrapper, lang: Lang) -> Generator[tuple[int, str]]:
    line_number = 0
    for line in file:
        line_number += 1
        line = line.strip()
        if line.startswith(lang.single_ln):
            yield line_number, line

