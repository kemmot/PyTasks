import filters.filterbase as filterbase


class AllBatchFilter(filterbase.FilterBase):
    def __init__(self):
        self._filters = []
    
    def add_filter(self, filter):
        self._filters.append(filter)

    def filter_items(self, items):
        for filter in self._filters:
            items = filter.filter_items(items)
        return items

    def is_match(self, task):
        for filter in self._filters:
            if not filter.is_match(task):
                return False
        return True
