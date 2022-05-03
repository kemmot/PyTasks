import filters.filterbase as filterbase


class AlwaysFilter(filterbase.FilterBase):
    @property
    def filter_group(self):
        return 'none'

    def is_match(self, task):
        return True
