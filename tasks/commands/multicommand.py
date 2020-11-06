import commands.commandbase as commandbase
import entities
import filters.allbatchfilter as allbatchfilter
import filters.alwaysfilter as alwaysfilter


class MultiCommand(commandbase.FilterCommandBase):
    def __init__(self, context, zero_item_action, one_item_action, multi_item_action):
        super().__init__(context)
        self._zero_item_action = zero_item_action
        self._one_item_action = one_item_action
        self._multi_item_action = multi_item_action

    def execute(self):
        '''
        Executes the logic of this command.
        '''
        tasks = self.get_filtered_tasks()
        task_count = len(tasks)
        if task_count == 0:
            self._execute_command(tasks, self._zero_item_action)
        elif task_count == 1:
            self._execute_command(tasks, self._one_item_action)
        else:
            self._execute_command(tasks, self._multi_item_action)
    
    def _execute_command(self, tasks, command):
        if command is None:
            raise Exception(f'Cannot process {len(tasks)} items in default command')
        command.execute(tasks)
