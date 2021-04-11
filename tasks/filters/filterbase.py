class FilterBase:
    def __init__(self, context):
        self._context = context
    
    @property
    def context(self):
        return self._context

    def filter_items(self, items):
        filtered_items = []
        for item in items:
            if self.is_match(item):
                filtered_items.append(item)
        return filtered_items

    def is_match(self, task):
        '''
        Executes the logic of this filter.
        '''
        raise Exception('is_match not implemented in {}'.format(self.__class__.__name__))


class BatchFilter(FilterBase):
    def __init__(self, context):
        super().__init__(context)
        self._filters = []

    @property
    def filters(self):
        return self._filters

    def add_filter(self, task_filter):
        self._filters.append(task_filter)

    def filter_items(self, items):
        filtered_items = []
        for item in items:
            if self.is_match(item):
                filtered_items.append(item)
        return filtered_items
    
    def __str__(self):
        description = self.__class__.__name__
        description += '('
        filter_index = 1
        for task_filter in self._filters:
            if filter_index > 1:
                description += ', '
            description += '[filter {}: {}]'.format(filter_index, task_filter)
            filter_index += 1
        description += ')'
        return description


class FilterParserBase:
    def parse(self, context, arg):
        '''
        Parses a filter from an argument.
        '''
        raise Exception('parse not implemented in {}'.format(__class__.__name__))
