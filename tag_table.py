from codetag import CodeTagInstance

class TagRow:
    def __init__(self, file_name: str, tag: CodeTagInstance):
        self.file_name = file_name
        self.line_num = str(tag.line_number)
        self.tag_name = tag.tag_name
        self.message = tag.message

class TagTable:
    def __init__(self, tag_list: list[TagRow]=[]):
        self._tags = tag_list
        self.view = tag_list

    def add_tag(self, tag: TagRow):
        self._tags.append(tag)

    def filename_sort(self):
        self.view = sorted(self.view, key=lambda tag: tag.file_name)

    def tag_name_sort(self):
        self.view = sorted(self.view, key=lambda tag: tag.tag_name)

    def filter_for_tag_type(self, *tag_type: str):
        filtered = []
        selected = {*tag_type}

        for tag in self.view:
            if tag.tag_name in selected:
                filtered.append(tag)

        self.view = filtered

    def hide_entries(self, *row_nums: int):
        chopping_block = []
        for i in row_nums:
            try:
                chopping_block.append(self.view[i])
            except IndexError:
                print(f"Error: row number {i} does not exist")

        for tag in chopping_block:
            self.view.remove(tag)

    def reset_view(self):
        self.view = self._tags

