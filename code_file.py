from enum import Enum
import git
from io import TextIOWrapper
from codetag import CodeTagInstance
from typing import Generator

class SrcLangType(Enum):
    # TODO: expand to more languages
    CLANG = ".c"
    CPP = ".cpp"
    CSHARP = ".cs"
    GOLANG = ".go"
    JAVA = ".java"
    JAVASCRIPT = ".js"
    LUA = ".lua"
    PHP = ".php"
    PYTHON = ".py"
    RUST = ".rs"
    TYPESCRIPT = ".ts"
    ZIG = ".zig"


class Lang:
    def __init__(self, lang_type: SrcLangType) -> None:
        self.name_of_lang = lang_type
        self.file_ext = lang_type.value
        self.single_ln = ""

        self.set_comment_syntax()

    def set_comment_syntax(self) -> None:
        match self.name_of_lang:
            case SrcLangType.CLANG | SrcLangType.CPP |SrcLangType.CSHARP | SrcLangType.GOLANG | SrcLangType.RUST | SrcLangType.JAVASCRIPT | SrcLangType.TYPESCRIPT | SrcLangType.JAVA | SrcLangType.PHP | SrcLangType.ZIG:
                self.single_ln = "//"

            case SrcLangType.LUA:
                self.single_ln = "--"

            case SrcLangType.PYTHON:
                self.single_ln = "#"

    def __repr__(self) -> str:
        return f"{self.name_of_lang.name}"

class CodeFile:
    def __init__(self, file_path: str, lang_type: SrcLangType) -> None:
        self._file_path = file_path
        self._lang = Lang(lang_type)
        self._commit = None

    @property
    def path(self):
        return self._file_path
    @property
    def lang(self):
        return self._lang
    @property
    def commit(self):
        return self._commit

    def extract_tagged_comments(self) -> list[CodeTagInstance]:
        with open(self.path) as f:
            tag_list = []
            current_tag = CodeTagInstance()
            for num_ln, comment in iterate_comments(f, self.lang):
                has_code_tag = current_tag.find_tag(comment, num_ln)
                if has_code_tag == True:
                    tag_list.append(current_tag)
                    current_tag = CodeTagInstance()
            return tag_list

class Project:
    def __init__(self, project_path: str) -> None:
        # NOTE: old arch is designed to look at files on the os and doesn't care about what's in version control.

        # TODO: capture only most recent commit. Pseudocode below:
            # If user attempts cmd with staged or untracked changes, show warning.
            # Once user commits and working tree is clean, process the files for tags.

        # TEST: if the tree property maintains state between commits

        self._repo: git.Repo = git.Repo(project_path)
        self._path: str = project_path
        assert not self._repo.bare, f"No git repository initialized at path {project_path}"
        self._source_code: list[CodeFile] = []

    @property
    def repo(self):
        return self._repo
    @property
    def path(self):
        return self._path
    @property
    def sourcecode(self):
        return self._source_code
    @property
    def tree(self):
        return self.repo.head.commit.tree
    @property
    def commit(self):
        return self.repo.head.commit

    def _get_files(self, root: git.Tree) -> list[CodeFile]:
        blobs = []
        for entry in root:
            if entry.type == "tree":
                blobs.extend(self._get_files(entry))
            file_type = infer_lang_type(entry.name)
            if file_type is not None:
                path_to_file = f"{self.path}{entry.path}"
                blobs.append(CodeFile(path_to_file, file_type))
        return blobs

    @property
    def files(self):
        return self._get_files(self.tree)

def infer_lang_type(filename: str) -> SrcLangType | None:
    for member in SrcLangType:
        if filename.endswith(member.value):
            return member
    return None


def iterate_comments(file: TextIOWrapper, lang: Lang) -> Generator[tuple[int, str]]:
    line_number = 0
    for line in file:
        line_number += 1
        line = line.strip()
        if line.startswith(lang.single_ln):
            yield line_number, line

