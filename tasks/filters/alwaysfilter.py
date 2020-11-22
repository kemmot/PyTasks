import filters.filterbase as filterbase


class AlwaysFilter(filterbase.FilterBase):
    def is_match(self, task):
        return True
