import logging
import filters.filterbase as filterbase


class TaskNameFilter(filterbase.FilterBase):
    def __init__(self, name):
        self._logger = logging.getLogger(__class__.__name__)
        self._name = name

    @property
    def name(self):
        return self._name

    def is_match(self, task):
        result = self._name.upper() in task.name.upper()
        self._logger.debug('is_match: {}, task: [{}]'.format(result, task))
        return result


class TaskNameFilterParser(filterbase.FilterParserBase):
    def parse(self, arg):
        if arg:
            search_term = arg
            if len(search_term) > 2 and search_term[0] == '/' and search_term[-1] == '/':
                search_term = search_term[1:-1]
            task_filter = TaskNameFilter(search_term)
        else:
            task_filter = None
        return task_filter
