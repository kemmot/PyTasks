import filters.filterbase as filterbase


class TaskIndexFilter(filterbase.FilterBase):
    def __init__(self, index):
        self._index = index

    @property
    def index(self):
        return self._index

    def is_match(self, task):
        return task.index == self._index


class TaskIndexFilterParser(filterbase.FilterParserBase):
    def parse(self, arg):
        if arg.isnumeric():
            task_filter = TaskIndexFilter(int(arg))
        else:
            task_filter = None
        return task_filter
