import os.path
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
        assert not self._repo.is_dirty, f"Make sure your git repository is clean"
        self._src_files: list[CodeFile] = []
        self._tagged_src_files: list[CodeFile] = []

    @property
    def src_files(self) -> list[CodeFile]:
        """
        Looks for source code files in the most recent commit found in project's git.
        If any are found, they are returned as CodeFile objects. If not, an exception is raised.
        """
        self._src_files = self._get_files(self.tree)
        if self._src_files == []:
            raise NoSrcFilesException
        return self._src_files

    @property
    def tagged_src_files(self) -> list[CodeFile]:
        """
        Gets only those source code files that have tags. If none of them do, raises an exception.
        """
        self._get_tagged_files()
        if self._tagged_src_files == []:
            raise NoTagsException
        return self._tagged_src_files

    @property
    def repo(self) -> Repo:
        """Returns the GitPython Repo object describing the git repo found in the current directory. If no repo is found, an error is raised."""
        return self._repo
    @property
    def path(self) -> str:
        """String representing the path that the Project has been told to look in."""
        return self._path
    @property
    def tree(self) -> Tree:
        """GitPython Tree object. Should always point to the project's root git tree in the latest commit."""
        return self.repo.head.commit.tree
    @property
    def commit_id(self) -> str:
        """Head commit hexsha."""
        return self.repo.head.commit.hexsha
    @property
    def name(self) -> str:
        """Name of project's root directory is assumed to be the project's name."""
        normed_path = os.path.normpath(self._path)
        tail = normed_path.rpartition('/')[-1]
        return tail


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
                path_to_file = f"{self.path}/{entry.path}"
                blob_hash = entry.hexsha
                code_file = CodeFile(file_name, path_to_file, lang_type, self.commit_id, blob_hash)
                blobs.append(code_file)
        return blobs

