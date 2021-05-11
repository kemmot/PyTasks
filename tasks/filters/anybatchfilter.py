import filters.filterbase as filterbase


class AnyBatchFilter(filterbase.BatchFilter):
    def is_match(self, task):
        for task_filter in self._filters:
            if task_filter.is_match(task):
                return True
        return False
