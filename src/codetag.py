from enum import Enum

class TagType(Enum):
    TODO = "TODO"
    FIXME = "FIXME"
    BUG = "BUG"
    DEBUG = "DEBUG"
    HACK = "HACK"
    NOTE = "NOTE"


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
        
