import commands.commandbase as commandbase


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
            if self._zero_item_action is None:
                raise Exception(f'Cannot process {len(tasks)} items in default command')
            self._zero_item_action.before_execute()
            self._zero_item_action.execute()
        elif task_count == 1:
            self._execute_command(tasks, self._one_item_action)
        else:
            self._execute_command(tasks, self._multi_item_action)

    def _execute_command(self, tasks, command):
        if command is None:
            raise Exception(f'Cannot process {len(tasks)} items in default command')
        try:
            command.before_execute()
            command.execute_tasks(tasks)
            self._logger.debug('Executed {} command on {} tasks'.format(command.__class__.__name__, len(tasks)))
        except Exception as ex:
            raise Exception(f'Failed executing {command}') from ex
