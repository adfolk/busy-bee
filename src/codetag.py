from enum import Enum

class TagType(Enum):
    # TODO: find out how to support keyword aliases
    TODO = {"TODO:"}
    FIX = {"FIX:", "FIXME:", "BUG:", "DEBUG:", "ISSUE:"}
    HACK = {"HACK:", "KLUDGE:"}
    PERF = {"OPTIMIZE:", "OPTIM:", "PERF:"}
    TEST = {"TESTING:", "FAILED:"}


class CodeTag:
    # TODO: information that this class should be able to carry:
    """
        - UID
        - Abs line number
        - TODO type
        - Git commit hash
        - parent filename
    """
    def __init__(self, tag_type: TagType, line_number: int, message: str) -> None:
        self.tag_type = tag_type
        self.line_number = line_number
        self.message = message
        
