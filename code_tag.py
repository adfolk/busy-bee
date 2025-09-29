from enum import Enum
from dataclasses import dataclass

class CodeTagEnum(Enum):
    BUG = {"FIX", "FIXME", "BUG", "DEBUG", "ISSUE"}
    HACK = {"HACK", "KLUDGE"}
    PERF = {"OPTIMIZE", "OPTIM", "PERF"}
    TEST = {"TEST", "TESTING", "FAILED"}
    TODO = {"TODO", "TASK"}
    WARN = {"WARNING", "WARN", "CAUTION"}

    @classmethod
    def which_tag(cls, word: str):
        for name, member in cls.__members__.items():
            if word in member.value:
                return cls(member)
        return None
    
@dataclass
class CodeTag:
    _tag_enum: CodeTagEnum
    line_number: int
    message: str
    parent_file_name: str
    commit_parent: str
    blob_parent: str

    @property
    def tag_name(self) -> str:
        return self._tag_enum.name
