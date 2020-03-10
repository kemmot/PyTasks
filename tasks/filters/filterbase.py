class FilterBase:
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
        raise Exception('is_match not implemented in {}'.format(__class__.__name__))


class FilterParserBase:
    def parse(self, arg):
        '''
        Parses a filter from an argument.
        '''
        raise Exception('parse not implemented in {}'.format(__class__.__name__))
