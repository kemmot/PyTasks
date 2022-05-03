import logging
import re

import filters.anybatchfilter as anybatchfilter
import filters.filterbase as filterbase


class TaskIndexFilter(filterbase.FilterBase):
    def __init__(self, context, index):
        super().__init__(context)
        self._index = index
        self._logger = logging.getLogger(__class__.__name__)

    @property
    def filter_group(self):
        return 'index'

    @property
    def index(self):
        return self._index

    def is_match(self, task):
        result = task.index == self._index
        self._logger.debug('is_match: {}, task: [{}]'.format(result, task))
        return result
    
    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, self.index)


class TaskIndexGreaterThanOrEqualFilter(filterbase.FilterBase):
    def __init__(self, context, index):
        super().__init__(context)
        self._index = index
        self._logger = logging.getLogger(__class__.__name__)

    @property
    def filter_group(self):
        return 'index'

    @property
    def index(self):
        return self._index

    def is_match(self, task):
        result = task.index >= self._index
        self._logger.debug('is_match: {}, task: [{}]'.format(result, task))
        return result
    
    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, self.index)


class TaskIndexLessThanOrEqualFilter(filterbase.FilterBase):
    def __init__(self, context, index):
        super().__init__(context)
        self._index = index
        self._logger = logging.getLogger(__class__.__name__)

    @property
    def filter_group(self):
        return 'index'

    @property
    def index(self):
        return self._index

    def is_match(self, task):
        result = task.index <= self._index
        self._logger.debug('is_match: {}, task: [{}]'.format(result, task))
        return result
    
    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, self.index)


class TaskIndexRangeFilter(filterbase.FilterBase):
    def __init__(self, context, start_index, end_index):
        if end_index <= start_index:
            raise Exception('End of range must be after start, start: {}, end: {}'.format(start_index, end_index))
        super().__init__(context)
        self._start_index = start_index
        self._end_index = end_index
        self._logger = logging.getLogger(__class__.__name__)

    @property
    def filter_group(self):
        return 'index'

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
        return '{}({}-{})'.format(self.__class__.__name__, self.start_index, self.end_index)


class TaskIndexFilterParser(filterbase.FilterParserBase):
    def parse(self, context, arg):
        task_filters = anybatchfilter.AnyBatchFilter(context)
        filter_count = 0
        for part in arg.split(','):
            task_filter = self._parse_range_filter(context, part)

            if not task_filter:
                task_filter = self._parse_single_number_filter(context, part)

            if not task_filter:
                task_filter = self._parse_greater_than_or_equal_filter(context, part)

            if not task_filter:
                task_filter = self._parse_less_than_or_equal_filter(context, part)

            if task_filter:
                task_filters.add_filter(task_filter)
                filter_count += 1
        
        if filter_count > 0:
            if filter_count > 1:
                return task_filters

            return task_filters.filters[0]
        
        return None

    def _parse_range_filter(self, context, arg):
        regex = re.compile(r'^(?P<start>\d+)-(?P<end>\d+)$', re.IGNORECASE)
        match = regex.search(arg)
        if match:
            start = int(match.group('start'))
            end = int(match.group('end'))
            return TaskIndexRangeFilter(context, start, end)
        
        return None

    def _parse_greater_than_or_equal_filter(self, context, arg):
        regex = re.compile(r'^(?P<index>\d+)-$', re.IGNORECASE)
        match = regex.search(arg)
        if match:
            index = int(match.group('index'))
            return TaskIndexGreaterThanOrEqualFilter(context, index)
        
        return None

    def _parse_less_than_or_equal_filter(self, context, arg):
        regex = re.compile(r'^-(?P<index>\d+)$', re.IGNORECASE)
        match = regex.search(arg)
        if match:
            index = int(match.group('index'))
            return TaskIndexLessThanOrEqualFilter(context, index)
        
        return None

    def _parse_single_number_filter(self, context, arg):
        if arg.isnumeric():
            value = int(arg)
            if value >= 0:
                return TaskIndexFilter(context, int(arg))
        
        return None
