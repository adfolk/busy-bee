from enum import Enum
import os
import git

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
    # TODO: change this class to represent a file
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
    def __init__(self, project_path: str, file_path: str, lang_type: SrcLangType) -> None:
        self.project_path = project_path
        self.file_path = file_path
        self.project_name = os.path.split(project_path)[1]
        self.file_name = os.path.split(file_path)[1]
        self.lang = Lang(lang_type)
        self.commit_hash = None

class Project:
    def __init__(self, project_path: str) -> None:
        # NOTE: old arch is designed to look at files on the os and doesn't care about what's in version control.

        # TODO: capture only most recent commit. Pseudocode below:
            # If user attempts cmd with staged or untracked changes, show warning.
            # Once user commits and working tree is clean, process the files for tags.

        # TEST: if the tree property maintains state between commits

        # NOTE: find out where GitPy keeps blob contents, or how to access a blob pointed to by Tree

        self.project_path: str = project_path
        self.repo: git.Repo = git.Repo(project_path)
        assert not self.repo.bare, f"No git repository initialized at path {project_path}"
        self.code_files: list[CodeFile] = []

    @property
    def tree(self):
        return self.repo.head.commit.tree

