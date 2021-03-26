import logging
import re

import filters.filterbase as filterbase


class TaskIndexFilter(filterbase.FilterBase):
    def __init__(self, context, index):
        super().__init__(context)
        self._index = index
        self._logger = logging.getLogger(__class__.__name__)

    @property
    def index(self):
        return self._index

    def is_match(self, task):
        result = task.index == self._index
        self._logger.debug('is_match: {}, task: [{}]'.format(result, task))
        return result
    
    def __str__(self):
        return 'TaskIndexFilter({})'.format(self.index)


class TaskIndexRangeFilter(filterbase.FilterBase):
    def __init__(self, context, start_index, end_index):
        if end_index <= start_index:
            raise Exception('End of range must be after start, start: {}, end: {}'.format(start_index, end_index))
        super().__init__(context)
        self._start_index = start_index
        self._end_index = end_index
        self._logger = logging.getLogger(__class__.__name__)

    @property
    def start_index(self):
        return self._start_index

    @property
    def end_index(self):
        return self._end_index

    def is_match(self, task):
        result = task.index >= self.start_index and task.index <= self.end_index
        self._logger.debug('is_match: {}, task: [{}]'.format(result, task))
        return result
    
    def __str__(self):
        return 'TaskIndexRangeFilter({}-{})'.format(self.start_index, self.end_index)


class TaskIndexFilterParser(filterbase.FilterParserBase):
    def parse(self, context, arg):
        regex = re.compile('^(?P<start>\d+)(-(?P<end>\d+))?$', re.IGNORECASE)
        match = regex.search(arg)
        if match != None:
            start = int(match.group('start'))
            end_text = match.group('end')
            if end_text != None:
                task_filter = TaskIndexRangeFilter(context, start, int(end_text))
            else:
                task_filter = TaskIndexFilter(context, start)
        else:
            task_filter = None
        return task_filter
