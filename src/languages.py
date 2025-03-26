from enum import Enum

class SrcLangType(Enum):
    CLANG_HDR = ".h"
    CLANG_SRC = ".c"
    GOLANG = ".go"
    JAVA = ".java"
    JAVASCRIPT = ".js"
    LUA = ".lua"
    PHP = ".php"
    PYTHON = ".py"
    RUST = ".rs"
    TYPESCRIPT = ".ts"
    ZIG = ".zig"


""" 
The Lang class will be used to set and retrieve the appropriate comment strings for any of the supported languages, which the search_src_file() function will pass to a regex function to create capture groups.
"""
class Lang:
    def __init__(self, lang_type: SrcLangType) -> None:
        self.lang_enum = lang_type      # WARNING: get_comment_syntax depends on this member
        self.nameof_lang = lang_type
        self.file_ext = lang_type.value
        self.single_ln = None
        self.multi_ln_op = None
        self.multi_ln_cl = None
        self.alt_single_ln = None

        self.set_comment_syntax()

    def set_comment_syntax(self) -> None:
        match self.lang_enum:
            # C-like comments
            case SrcLangType.CLANG_HDR | SrcLangType.CLANG_SRC | SrcLangType.GOLANG | SrcLangType.RUST | SrcLangType.JAVASCRIPT | SrcLangType.TYPESCRIPT | SrcLangType.JAVA:
                self.single_ln = "//"
                self.multi_ln_op= "/*"
                self.multi_ln_cl = "*/"
            # Python
            case SrcLangType.PYTHON:
                self.single_ln = "#"
                self.multi_ln_op = '"""'
                self.multi_ln_cl = '"""'
            # PHP is weird lol
            case SrcLangType.PHP:
                self.single_ln = "//"
                self.multi_ln_op = "/*"
                self.multi_ln_cl = "*/"
                self.alt_single_ln = "#"

    def __repr__(self) -> str:
        return f"File extension: {self.file_ext}\nSingle line comments: {self.single_ln}\nMulti line opener: {self.multi_ln_op}\nMulti line closer: {self.multi_ln_cl}\nalt: {self.alt_single_ln}"

