from enum import Enum
import git
from io import TextIOWrapper
from code_tag import CodeTag, TagInstance
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
        self.name_of_lang: SrcLangType = lang_type
        self.file_ext: str = lang_type.value
        self.comment_symbol: str = self._get_comment_syntax()

    def _get_comment_syntax(self) -> str:
        match self.name_of_lang:
            case SrcLangType.CLANG | SrcLangType.CPP |SrcLangType.CSHARP | SrcLangType.GOLANG | SrcLangType.RUST | SrcLangType.JAVASCRIPT | SrcLangType.TYPESCRIPT | SrcLangType.JAVA | SrcLangType.PHP | SrcLangType.ZIG:
                return "//"

            case SrcLangType.LUA:
                return "--"

            case SrcLangType.PYTHON:
                return "#"

    def __repr__(self) -> str:
        return f"{self.name_of_lang.name}"

class CodeFile:
    def __init__(self, file_path: str, lang_type: SrcLangType, commit_hash: int, blob_hash: int) -> None:
        self._file_path = file_path
        self._lang = Lang(lang_type)
        self._commit = commit_hash
        self._blob_id = blob_hash
        self._tags = self._extract_tagged_comments()

    @property
    def path(self):
        return self._file_path
    @property
    def lang(self):
        return self._lang
    @property
    def commit(self):
        return self._commit
    @property
    def blob(self):
        return self._blob_id

    def _extract_tagged_comments(self) -> list[TagInstance]:
        with open(self.path) as f:
            tag_list = []
            for num_ln, comment in iterate_comments(f, self.lang):
                separated_text = comment.split(':', maxsplit=1)
                if len(separated_text) > 1:
                    tag_type = CodeTag.which_tag(separated_text[0])
                    if tag_type != None:
                        tag_list.append(TagInstance(tag_type, num_ln, separated_text[1]))
            return tag_list

    @property
    def tags(self):
        return self._tags

class Project:
    def __init__(self, project_path: str) -> None:
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
            if file_type != None:
                path_to_file = f"{self.path}{entry.path}"
                commit_hash = entry.commit_id
                blob_hash = entry.blob_id
                blobs.append(CodeFile(path_to_file, file_type, commit_hash, blob_hash))
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
        if line.startswith(lang.comment_symbol):
            yield line_number, line

