from git import Repo, Tree
from code_file import CodeFile, NoTagsException
from src_lang import SrcLang

class Project:
    def __init__(self, project_path: str) -> None:
        """
        Looks at a path and tries to figure out if an initialized git repo exists.
        If it does, it recursively looks through the repo for source code files.

        The Project.files property will return a list of tagged files if they exist, or None if no tags are found.
        """

        # TODO: figure out how to detect when working tree not clean w/nothing to commit
        # If user attempts cmd with staged or untracked changes, show warning.
        # Once user commits and working tree is clean, process the files for tags.

        # TEST: if the tree property tracks state between commits

        self._repo: Repo = Repo(project_path)
        self._path: str = project_path
        assert not self._repo.bare, f"No git repository initialized at path {project_path}"
        self._src_files: list[CodeFile] | type[NoTagsException] | None = None

    @property
    def src_files(self):
        """
        Looks for source code files in the most recent commit found in project's git and returns CodeFile objects, but only if all of the following conditions are met:
            * Source code files with supported file extensions can be found
            * Source code files contain code tags (e.g., TODO, BUG, FIX, etc.)
        """

        # TODO: handle "no tags" vs "no supported source files"
        # New "tagged files" property, separate from src_files
        # "src_files" should raise "NoSrcFilesException"
        # "tagged_files" should raise "NoTagsException"

        self._src_files = self._get_files(self.tree)
        if self._src_files == None:
            raise ValueError("No supported source code files found")
        return self._src_files

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

    def _get_files(self, root: Tree) -> list[CodeFile] | type[NoTagsException]:
        tagged_files = self._r_get_files(root)
        if tagged_files != []:
            return tagged_files
        return NoTagsException

    def _r_get_files(self, root: Tree) -> list[CodeFile]:
        # TODO: separate code_file.tags check so that no tags condition can be separated from no srcfile condition
        blobs = []
        for entry in root:
            if entry.type == "tree":
                blobs.extend(self._r_get_files(entry))
            file_name = entry.name
            lang_type = SrcLang.get_lang(file_name)
            if lang_type != None:
                path_to_file = f"{self.path}{entry.path}"
                commit_hash = entry.commit_id
                blob_hash = entry.blob_id
                code_file = CodeFile(file_name, path_to_file, lang_type, commit_hash, blob_hash)
                if code_file.tags != NoTagsException:
                    blobs.append(code_file)
        return blobs

