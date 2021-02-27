import logging
import filters.filterbase as filterbase


class TaskIndexFilter(filterbase.FilterBase):
    def __init__(self, index):
        self._index = index
        self._logger = logging.getLogger(__class__.__name__)

    @property
    def index(self):
        return self._index

    def is_match(self, task):
        result = task.index == self._index
        self._logger.debug('is_match: {}, task: [{}]'.format(result, task))
        return result


class TaskIndexFilterParser(filterbase.FilterParserBase):
    def parse(self, arg):
        if arg.isnumeric():
            task_filter = TaskIndexFilter(int(arg))
        else:
            task_filter = None
        return task_filter
