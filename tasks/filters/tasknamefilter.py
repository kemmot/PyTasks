import filters.filterbase as filterbase


class TaskNameFilter(filterbase.FilterBase):
    def __init__(self, name):
        self._name = name
    
    @property
    def name(self):
        return self._name

    def is_match(self, task):
        return self._name.upper() in task.name.upper()


class TaskNameFilterParser(filterbase.FilterParserBase):
    def parse(self, arg):
        if arg:
            filter = TaskNameFilter(arg)
        else:
            filter = None
        return filter
