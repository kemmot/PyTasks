'''
A module providing task commands.
'''

import datetime
import logging
import uuid

import entities


class CommandFactory:
    def __init__(self, storage):
        self._storage = storage

    def get_command(self, args):
        command = None
        if args.command == 'add':
            task = entities.Task()
            task.created = datetime.datetime.now()
            task.id_number = uuid.uuid4()
            task.name = ' '.join(args.name)
            task.status = 'pending'

            command = AddTaskCommand(self._storage)
            command.task = task
        elif args.command == 'list':
            command = ListTaskCommand(self._storage)
        else:
            raise Exception('Command not recognised: [{}]'.format(args.command))

        return command


class CommandBase:
    '''
    A base class providing functionality common to all commands.
    '''
    def __init__(self, storage):
        self._logger = logging.getLogger(__class__.__name__)
        self._storage = storage

    @property
    def storage(self):
        '''
        The storage to write the task to.
        '''
        return self._storage

    @storage.setter
    def storage(self, value):
        self._storage = value

    def execute(self):
        '''
        Executes the logic of this command.
        '''
        raise Exception('Execute not implemented in {}'.format(__class__.__name__))


class AddTaskCommand(CommandBase):
    '''
    A command that will add a task.
    '''
    def __init__(self, storage):
        super().__init__(storage)
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
        self._storage.write(self.task)
        self._logger.info('Created task')


class ListTaskCommand(CommandBase):
    '''
    A command that will list tasks.
    '''

    def execute(self):
        '''
        Executes the logic of this command.
        '''
        print('ID   Status  Description')
        print('------------------------')
        for task in self.storage.read_all():
            format_string = '{} {} {}'
            print(format_string.format( \
                    task.index, \
                    task.status, \
                    task.name))
