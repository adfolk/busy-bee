from functools import total_ordering


@total_ordering
class CodeTagInstance():
    def __init__(self):
        self._tag_dict = {
                "FIX": ["FIX", "FIXME", "BUG", "DEBUG", "ISSUE"],
                "HACK": ["HACK", "KLUDGE"],
                "PERF": ["OPTIMIZE", "OPTIM", "PERF"],
                "TEST": ["TESTING", "FAILED"],
                "TODO": ["TODO"],
                "WARNING": ["WARNING", "WARN", "CAUTION"]
        }
        self.tag_name = ""
        self.line_number = 0
        self.message = ""

    def find_tag(self, text_string: str, line_num: int) -> bool:
        separated_text = text_string.split(':', maxsplit=1)
        if len(separated_text) == 1:    # if no matches are found
            return False
        for key, alias_list in self._tag_dict.items():
            for item in alias_list:
                if item in separated_text[0]:
                    self.tag_name = key
                    self.line_number = line_num
                    self.message = separated_text[1].strip()
                    return True
        return False

    def __str__(self) -> str:
        return f"Line: {self.line_number}, Tag: {self.tag_name}, Message: {self.message}"

    def __eq__(self, other):
        return (self.line_number == other.line_number)

    def __lt__(self, other):
        return self.line_number < other.line_number

