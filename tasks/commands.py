'''
A module providing task commands.
'''

import datetime
import logging
import uuid

import entities
import formatters


class CommandFactory:
    def __init__(self, filename):
        self._filename = filename

    def get_command(self, args):
        command = None
        if args.command == 'add':
            task = entities.Task()
            task.created = datetime.datetime.now()
            task.id_number = uuid.uuid4()
            task.name = ' '.join(args.name)
            task.status = 'pending'

            formatter = formatters.TaskWarriorFormatter()

            command = AddTaskCommand(formatter)
            command.filename = self._filename
            command.task = task
        elif args.command == 'list':
            formatter = formatters.TaskWarriorFormatter()
            command = ListTaskCommand(formatter)
            command.filename = self._filename
        else:
            raise Exception('Command not recognised: [{}]'.format(args.command))

        return command


class CommandBase:
    '''
    A base class providing functionality common to all commands.
    '''
    def __init__(self):
        self._logger = logging.getLogger(__class__.__name__)
        self._filename = ''

    @property
    def filename(self):
        '''
        The name of the file to write the task to.
        '''
        return self._filename

    @filename.setter
    def filename(self, value):
        self._filename = value

    def execute(self):
        '''
        Executes the logic of this command.
        '''
        raise Exception('Execute not implemented in {}'.format(__class__.__name__))


class AddTaskCommand(CommandBase):
    '''
    A command that will add a task.
    '''
    def __init__(self, formatter):
        super().__init__()
        self._formatter = formatter
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
        with open(self.filename, 'a+') as file:
            formatted_task = self._formatter.format(self.task)
            file.write(formatted_task + '\n')
        self._logger.info('Created task')


class ListTaskCommand(CommandBase):
    '''
    A command that will list tasks.
    '''

    def __init__(self, formatter):
        super().__init__()
        self._formatter = formatter

    def execute(self):
        '''
        Executes the logic of this command.
        '''
        with open(self.filename, 'r') as file:
            print('ID   Status  Description')
            print('------------------------')
            line_number = 1
            for line in file.readlines():
                line = line.strip()
                task = self._formatter.parse(line_number, line)
                format_string = '{} {} {}'
                print(format_string.format( \
                        task.index, \
                        task.status, \
                        task.name))
                line_number += 1
