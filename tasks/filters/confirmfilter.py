import filters.filterbase as filterbase


class ConfirmFilter(filterbase.FilterBase):
    def __init__(self, context, action_name):
        super().__init__(context)
        self._action_name = action_name

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
        message = '{}? [y/n]... ID: {}, name: "{}"> '.format( \
            self.action_name, \
            task.index, \
            task.name)
        return self._query(message)
    
    def _query_multiple(self, tasks):
        message = '{}? [y/n]... {} items> '.format(self.action_name, len(tasks))
        return self._query(message)
    
    def _query(self, message):
        if self.context.console.input(message).startswith('y'):
            return True
        return False
