import filters.filterbase as filterbase


class ConfirmFilter(filterbase.FilterBase):
    def __init__(self, action_name):
        self._action_name = action_name
    
    @property
    def action_name(self):
        return self._action_name

    def filter_items(self, items):
        filtered_items = []
        if len(items) > 0:
            if len(items) == 1:
                message = '{}? [y/n]... ID: {}, name: {}'.format(self.action_name, items[0].index, items[0].name)
            else:
                message = '{}? [y/n]... {} items'.format(self.action_name, len(items))
            print(message)
            if input().startswith('y'):
                filtered_items = items
            else:
                filtered_items = []
        else:
            # no prompt required
            filtered_items = items
        
        return filtered_items
