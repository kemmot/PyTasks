'''
A module providing task commands.
'''

import entities
import formatters
import logging


class CommandFactory:
    def __init__(self, filename):
        self._filename = filename
    
    def get_command(self, args):
        command = None
        if args.command == 'add':
            task = entities.Task()
            task.name = ' '.join(args.name)
            
            formatter = formatters.TaskWarriorFormatter()

            command = AddTaskCommand(formatter)
            command.filename = self._filename
            command.task = task
        else:
            raise Exception('Command not recognised: [{}]'.format(args.command))
        return command


class AddTaskCommand:
    '''
    A command that will add a task.
    '''
    def __init__(self, formatter):
        self._logger = logging.getLogger(__class__.__name__)
        self._formatter = formatter
        self._filename = ''
        self._task = None

    @property
    def filename(self):
        '''
        The name of the file to write the task to.
        '''
        return self._filename

    @filename.setter
    def filename(self, value):
        self._filename = value

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
        with open(self.filename, 'a+') as file:
            formatted_task = self._formatter.format(self.task)
            file.write(formatted_task + '\n')
        self._logger.info('Created task')
