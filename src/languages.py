from enum import Enum

class SrcLangType(Enum):
    PYTHON = ".py",
    CLANG_SRC = ".c",
    CLANG_HDR = ".h",
    GOLANG = ".go",
    LUA = ".lua",
    RUST = ".rs"

