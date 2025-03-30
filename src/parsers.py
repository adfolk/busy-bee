from typing import Generator
from languages import Lang, CommentFamily

def extract_todo(filename: str, lang: Lang) -> tuple[list, list]:
    with open(filename) as f:
        comment_lines = []
        todos = []
        for num_ln, comment in iterate_comments(f, lang):
            print(comment)
            comment_lines.append([num_ln, comment])
            if "TODO:" in comment:
                todos.append([num_ln, comment])

        return comment_lines, todos


def iterate_comments(file, lang: Lang) -> Generator[tuple[int, str]]:
    num_ln = 0
    inMulti = False
    for line in file:
        num_ln += 1
        line = line.strip()
        if line.startswith(lang.single_ln):
            yield num_ln, line
        if lang.comment_type == CommentFamily.MULTI:
            if line.startswith(lang.multi_ln_op):
                yield num_ln, line
                inMulti = True
            elif inMulti == True:
                yield num_ln, line
                if lang.multi_ln_cl in line:
                    inMulti = False
        else:
            continue

