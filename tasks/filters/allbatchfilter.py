import filters.filterbase as filterbase


class AllBatchFilter(filterbase.FilterBase):
    def __init__(self, context):
        super().__init__(context)
        self._filters = []

    def add_filter(self, task_filter):
        self._filters.append(task_filter)

    def filter_items(self, items):
        for task_filter in self._filters:
            items = task_filter.filter_items(items)
        return items

    def is_match(self, task):
        for task_filter in self._filters:
            if not task_filter.is_match(task):
                return False
        return True
    
    def __str__(self):
        description = 'AllBatchFilter('
        filter_index = 1
        for task_filter in self._filters:
            if filter_index > 1:
                description += ', '
            description += '[filter {}: {}]'.format(filter_index, task_filter)
            filter_index += 1
        description += ')'
        return description
