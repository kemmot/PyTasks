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
            search_term = arg
            if len(search_term) > 2 and search_term[0] == '/' and search_term[-1] == '/':
                search_term = search_term[1:-1]
            filter = TaskNameFilter(search_term)
        else:
            filter = None
        return filter
