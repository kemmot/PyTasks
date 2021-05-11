import filters.filterbase as filterbase


class AllBatchFilter(filterbase.BatchFilter):
    def is_match(self, task):
        for task_filter in self._filters:
            if not task_filter.is_match(task):
                return False
        return True
