import commandline
import commands.commandbase as commandbase
#from tasks.commands.commandbase import FilterCommandBase


class MultiCommand(commandbase.FilterCommandBase):
    def __init__(self, context, zero_item_action, one_item_action, multi_item_action):
        super().__init__(context)
        self._zero_item_action = zero_item_action
        self._one_item_action = one_item_action
        self._multi_item_action = multi_item_action

    @property
    def zero_item_action(self):
        return self._zero_item_action

    @property
    def one_item_action(self):
        return self._one_item_action

    @property
    def multi_item_action(self):
        return self._multi_item_action

    def execute(self):
        '''
        Executes the logic of this command.
        '''
        tasks = self.get_filtered_tasks()
        task_count = len(tasks)
        
        if task_count == 0:
            command = self._zero_item_action
        elif task_count == 1:
            command = self._one_item_action
        else:
            command = self._multi_item_action
        
        if command is None:
            raise Exception(f'Cannot process {len(tasks)} items in default command')

        # need to allow the individual commands reload the tasks as garbage collection may change the indexes
        
        self._execute_command(command)

    def _execute_command(self, command):
        command.filter = self.filter        
        try:
            command.before_execute()
            command.execute()
        except commandline.ExitCodeException:
            raise
        except Exception as ex:
            raise Exception(f'Failed executing {command}') from ex
