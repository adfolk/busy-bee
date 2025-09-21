from dataclasses import dataclass
from enum import Enum
from functools import total_ordering

class TagCat(Enum):
    FIX = "FIX"
    HACK = "HACK"
    PERF = "PERF"
    TEST = "TEST"
    TODO = "TODO"
    WARNING = "WARNING"

    @classmethod
    def which_tag(cls, msg: str):
        pass


# def find_tag(text_string: str, line_num: int) -> bool:
#     separated_text = text_string.split(':', maxsplit=1)
#     if len(separated_text) == 1:    # if no matches are found
#         return False
#     for key, alias_list in self._tag_dict.items():
#         for item in alias_list:
#             if item in separated_text[0]:
#                 self.tag_name = key
#                 self.line_number = line_num
#                 self.message = separated_text[1].strip()
#                 return True
#     return False

# class CodeTagInstance():
#     def __init__(self):
#         self._tag_dict = {
#                 FIX: ["FIX", "FIXME", "BUG", "DEBUG", "ISSUE"],
#                 HACK: ["HACK", "KLUDGE"],
#                 PERF: ["OPTIMIZE", "OPTIM", "PERF"],
#                 TEST: ["TEST", "TESTING", "FAILED"],
#                 TODO: ["TODO"],
#                 WARNING: ["WARNING", "WARN", "CAUTION"]
#         }
#         self.tag_name = ""
#         self.line_number = 0
#         self.message = ""


