import datetime
import uuid

import commands.commandbase as commandbase
import entities


class AddTaskCommand(commandbase.CommandBase):
    '''
    A command that will add a task.
    '''
    def __init__(self, context):
        super().__init__(context)
        self._task = None

    @property
    def task(self):
        '''
        The task to add.
        '''
        return self._task

    @task.setter
    def task(self, value):
        self._task = value

    def execute(self):
        '''
        Executes the logic of this command.
        '''
        key_id = self.context.settings.command_add_next_key_id
        mappings = {
            'key_id': key_id,
            'name': self.task.name
        }
        self.task.name = self.context.settings.command_add_format.format(**mappings)

        existing_tasks = self.context.storage.read_all()
        self.context.storage.write(self.task)
        self.context.settings.command_add_next_key_id = key_id + 1
        self.task.index = len(existing_tasks) + 1
        print('Task created: {}'.format(self.task.index))


class AddTaskCommandParser(commandbase.CommandParserBase):
    COMMAND_NAME = 'add'

    def __init__(self):
        super().__init__(AddTaskCommandParser.COMMAND_NAME)

    def parse(self, context, args):
        if not args:
            raise Exception('Adding new task requires at least one word in name')

        task = entities.Task()
        task.created = datetime.datetime.now()
        task.id_number = uuid.uuid4()
        task.name = ' '.join(args)
        task.status = 'pending'

        command = AddTaskCommand(context)
        command.task = task
        return command
