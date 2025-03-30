from enum import Enum, Flag

class SrcLangType(Enum):
    # TODO: expand to more languages
    CLANG = ".c"    # not going to support header.h files for now.
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

class CommentFamily(Flag):
    SINGLE_ONLY = 1
    MULTI = 2


""" 
The Lang class will be used to set and retrieve the appropriate comment strings for any of the supported languages, which the search_src_file() function will pass to a regex function to create capture groups.
"""
class Lang:
    def __init__(self, lang_type: SrcLangType) -> None:
        self.name_of_lang = lang_type      # WARNING: set_comment_syntax depends on this member
        self.file_ext = lang_type.value
        self.single_ln = ""
        self.multi_ln_op = None
        self.multi_ln_cl = None
        self.alt_single_ln = None
        self.special_char = None
        self.comment_type = None

        self.set_comment_syntax()

    def set_comment_syntax(self) -> None:
        match self.name_of_lang:
            # C-style comments
            case SrcLangType.CLANG | SrcLangType.CPP |SrcLangType.CSHARP | SrcLangType.GOLANG | SrcLangType.RUST | SrcLangType.JAVASCRIPT | SrcLangType.TYPESCRIPT | SrcLangType.JAVA:
                self.single_ln = "//"
                self.multi_ln_op= "/*"
                self.multi_ln_cl = "*/"
                self.comment_type = CommentFamily.MULTI

            case SrcLangType.LUA:
                self.single_ln = "--"
                self.multi_ln_op = "--[["
                self.multi_ln_cl = "--]]"
                # adding a third '-' to any lua comment opener makes the code runnable again.
                # TODO: write special handler for lua
                self.special_char = "---"
                self.comment_type = CommentFamily.MULTI

            case SrcLangType.PYTHON:
                # multi-line comments (aka docstrings) in Python are seemingly interpreted strangely by Python's iteration mechanics. 
                # folke/todo-comments also does not support putting code tags in the middle of python docstrings. 
                # Will assume code tags will be put on single lines.
                self.single_ln = "#"
                self.comment_type = CommentFamily.SINGLE_ONLY
                
            case SrcLangType.PHP:
                # Will not support "#" comments for PHP since standard usage is to use "//".
                self.single_ln = "//"
                self.multi_ln_op = "/*"
                self.multi_ln_cl = "*/"
                self.comment_type = CommentFamily.MULTI

            case SrcLangType.ZIG:
                # zig only does docstrings and single line comments. No C-style multiline comments.
                self.single_ln = "//"
                self.comment_type = CommentFamily.SINGLE_ONLY

    def __repr__(self) -> str:
        return f"{self.name_of_lang.name}"

        # NOTE: keeping this in case I want to print all the values later

        #return f"File extension: {self.file_ext}\nSingle line comments: {self.single_ln}\nMulti line opener: {self.multi_ln_op}\nMulti line closer: {self.multi_ln_cl}\nalt: {self.alt_single_ln}"

