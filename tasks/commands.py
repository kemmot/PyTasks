'''
A module providing task commands.
'''

import datetime
import logging
import uuid

import entities


class CommandFactory:
    def __init__(self, storage):
        self._commands = {}
        self._storage = storage
        self._register_commands()
    
    def _register_commands(self):
        self._register_command('add', AddTaskCommand(self._storage))
        self._register_command('list', ListTaskCommand(self._storage))
    
    def _register_command(self, name, command):
        self._commands[name] = command

    def get_command(self, args):
        if not args.command in self._commands:
            raise Exception('Command not recognised: [{}]'.format(args.command))

        command = self._commands[args.command]
        if args.command == 'add':
            task = entities.Task()
            task.created = datetime.datetime.now()
            task.id_number = uuid.uuid4()
            task.name = ' '.join(args.name)
            task.status = 'pending'
            command.task = task

        return command
    
    def _populate_command(self, args, command):
        pass


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
