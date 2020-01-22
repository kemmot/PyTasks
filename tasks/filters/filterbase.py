class FilterBase:
    def is_match(self, task):
        '''
        Executes the logic of this filter.
        '''
        raise Exception('is_match not implemented in {}'.format(__class__.__name__))
