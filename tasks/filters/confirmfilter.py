import filters.filterbase as filterbase


class ConfirmFilter(filterbase.FilterBase):
    def __init__(self, context, action_name):
        super().__init__(context)
        self._action_name = action_name
        self._all_confirm = False
        self._all_deny = False

    @property
    def action_name(self):
        return self._action_name

    @property
    def filter_group(self):
        return 'user'

    def filter_items(self, tasks):
        filtered_tasks = []
        if tasks:
            if len(tasks) == 1:
                result = self._query_single(tasks[0])
            else:
                result = self._query_multiple(tasks)

            if result:
                filtered_tasks = tasks
            else:
                filtered_tasks = []
        else:
            # no prompt required
            filtered_tasks = tasks

        return filtered_tasks
    
    def is_match(self, task):
        return self._query_single(task)
    
    def _query_single(self, task):
        if self._all_confirm: return True
        if self._all_deny: return False
        
        message = '{}? [y]es/[n]o/[a]ll/[z]ero... ID: {}, name: "{}"> '.format( \
            self.action_name, \
            task.index, \
            task.name)
        return self.query(message)
    
    def _query_multiple(self, tasks):
        message = '{}? [y/n]... {} items> '.format(self.action_name, len(tasks))
        return self.query(message)
    
    def query(self, message=None):
        if not message:
            message = '{}? [y/n]>'.format(self.action_name)
        input = self.context.console.input(message)
        if input.startswith('y'):
            return True
        if input.startswith('a'):
            self._all_confirm = True
            return True
        if input.startswith('z'):
            self._all_deny = True
            return False
        return False
