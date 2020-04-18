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
        existing_tasks = self.context.storage.read_all()
        self.context.storage.write(self.task)
        self.task.index = len(existing_tasks) + 1
        print('Task created: {}'.format(self.task.index))


class AddTaskCommandParser(commandbase.CommandParserBase):
    def parse(self, context, args):
        if args[0] == 'add':
            if len(args) < 2:
                raise Exception('Add command requires task description')

            name = args[1:]

            task = entities.Task()
            task.created = datetime.datetime.now()
            task.id_number = uuid.uuid4()
            task.name = ' '.join(name)
            task.status = 'pending'

            command = AddTaskCommand(context)
            command.task = task
        else:
            command = None
        return command
