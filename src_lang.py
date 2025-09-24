from enum import Enum

class SrcLangType(Enum):
    # TODO: expand to more languages
    CLANG = ".c"
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

    @classmethod
    def infer_lang_type(cls, filename: str):
        for member in SrcLangType:
            if filename.endswith(member.value):
                return member
        return None


class SrcLang:
    def __init__(self, lang_type: SrcLangType) -> None:
        self.name_of_lang: SrcLangType = lang_type
        self.file_ext: str = lang_type.value
        self.comment_symbol: str = self._get_comment_syntax()

    def _get_comment_syntax(self) -> str:
        match self.name_of_lang:
            case SrcLangType.CLANG | SrcLangType.CPP |SrcLangType.CSHARP | SrcLangType.GOLANG | SrcLangType.RUST | SrcLangType.JAVASCRIPT | SrcLangType.TYPESCRIPT | SrcLangType.JAVA | SrcLangType.PHP | SrcLangType.ZIG:
                return "//"

            case SrcLangType.LUA:
                return "--"

            case SrcLangType.PYTHON:
                return "#"

    @staticmethod
    def get_lang(file_name: str):
        lang_type = SrcLangType(file_name)
        if lang_type != None:
            return SrcLang(lang_type)
        return None

    def __repr__(self) -> str:
        return f"{self.name_of_lang.name}"

