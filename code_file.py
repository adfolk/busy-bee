from code_tag import CodeTagEnum, CodeTag
from io import TextIOWrapper
from src_lang import SrcLang
from typing import Generator

class NoTagsException(Exception):
    """No code tags found."""

class CodeFile:
    def __init__(self, file_name: str, file_path: str, lang_type: SrcLang, commit_hash: int, blob_hash: int) -> None:
        self._file_name = file_name
        self._file_path = file_path
        self._lang = lang_type
        self._commit = commit_hash
        self._blob_id = blob_hash
        self._tags: list[CodeTag] | type[NoTagsException] = self._extract_tagged_comments()

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
    @property
    def file_name(self):
        return self._file_name
    @property
    def tags(self):
        return self._tags

    # API methods

    # Private implementation and helper methods
    def _extract_tagged_comments(self) -> list[CodeTag] | type[NoTagsException]:
        with open(self.path) as f:
            tag_list = []
            for num_ln, comment in self._iterate_comments(f, self.lang):
                separated_text = comment.split(':', maxsplit=1)
                if len(separated_text) > 1:
                    tag_type = CodeTagEnum.which_tag(separated_text[0])
                    tag_text = separated_text[1]
                    if tag_type != None:
                        tag_list.append(CodeTag(tag_type, num_ln, tag_text, self.file_name, self.commit, self.blob))
            if tag_list == []:
                return NoTagsException
            return tag_list

    @staticmethod
    def _iterate_comments(file: TextIOWrapper, lang: SrcLang) -> Generator[tuple[int, str]]:
        line_number = 0
        for line in file:
            line_number += 1
            line = line.strip()
            if line.startswith(lang.comment_symbol):
                yield line_number, line

