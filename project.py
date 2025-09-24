from git import Repo, Tree
from code_file import CodeFile
from src_lang import SrcLang

class NoSrcFilesException(Exception):
    """No source code files found in project repo."""

class NoTagsException(Exception):
    """No code tags were found in this project."""

class Project:
    def __init__(self, project_path: str) -> None:
        """
        Looks at a path and tries to figure out if an initialized git repo exists.
        If it does, it recursively looks through the repo for source code files.

        The Project.files property will return a list of tagged files if they exist, or None if no tags are found.
        """

        # TODO: figure out how to detect when working tree not clean w/nothing to commit
        # If user attempts cmd with staged or untracked changes, show warning.

        # TEST: if the tree property tracks state between commits

        self._repo: Repo = Repo(project_path)
        self._path: str = project_path
        assert not self._repo.bare, f"No git repository initialized at path {project_path}"
        self._src_files: list[CodeFile] = []
        self._tagged_src_files: list[CodeFile] = []

    @property
    def src_files(self):
        """
        Looks for source code files in the most recent commit found in project's git.
        If any are found, they are returned as CodeFile objects. If not, an exception is raised.
        """
        self._src_files = self._get_files(self.tree)
        if self._src_files == []:
            raise NoSrcFilesException
        return self._src_files

    @property
    def tagged_src_files(self):
        """
        Gets only those source code files that have tags. If none of them do, raises an exception.
        """
        self._get_tagged_files()
        if self._tagged_src_files == []:
            raise NoTagsException
        return self._tagged_src_files

    @property
    def repo(self):
        return self._repo
    @property
    def path(self):
        return self._path
    @property
    def tree(self):
        return self.repo.head.commit.tree
    @property
    def commit(self):
        return self.repo.head.commit

    def _get_tagged_files(self):
        for src_file in self.src_files:
            tags = src_file.tags
            if tags != []:
                self._tagged_src_files.append(src_file)

    def _get_files(self, root: Tree) -> list[CodeFile]:
        src_files = self._r_get_files(root)
        return src_files

    def _r_get_files(self, root: Tree) -> list[CodeFile]:
        blobs = []
        for entry in root:
            if entry.type == "tree":
                blobs.extend(self._r_get_files(entry))
            file_name = entry.name
            lang_type = SrcLang.get_lang(file_name)
            if lang_type != None:
                path_to_file = f"{self.path}{entry.path}"
                commit_hash = self.commit.hexsha
                blob_hash = entry.hexsha
                code_file = CodeFile(file_name, path_to_file, lang_type, commit_hash, blob_hash)
                blobs.append(code_file)
        return blobs

