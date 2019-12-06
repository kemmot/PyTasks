'''
A module providing task commands.
'''

import datetime
import logging
import uuid

import entities


class CommandFactory:
    def __init__(self, storage):
        self._parsers = {}
        self._storage = storage

    def register_known_parsers(self):
        for cla in CommandParserBase.__subclasses__():
            self.register_parser(cla())

    def register_parser(self, parser):
        self._parsers[parser.get_name()] = parser

    def get_command(self, args):
        if not args.command in self._parsers:
            raise Exception('Command not recognised: [{}]'.format(args.command))

        parser = self._parsers[args.command]
        return parser.parse(self._storage, args)


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


class CommandParserBase:
    def get_name(self):
        raise Exception('get_name not implemented in {}'.format(__class__.__name__))

    def parse(self, storage, args):
        raise Exception('parse not implemented in {}'.format(__class__.__name__))


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
        existing_tasks = self._storage.read_all()
        self._storage.write(self.task)
        self.task.index = len(existing_tasks) + 1
        print('Task created: {}'.format(self.task.index))


class AddTaskCommandParser(CommandParserBase):
    def get_name(self):
        return 'add'

    def parse(self, storage, args):
        task = entities.Task()
        task.created = datetime.datetime.now()
        task.id_number = uuid.uuid4()
        task.name = ' '.join(args.name)
        task.status = 'pending'

        command = AddTaskCommand(storage)
        command.task = task
        return command


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


class ListTaskCommandParser(CommandParserBase):
    def get_name(self):
        return 'list'

    def parse(self, storage, args):
        return ListTaskCommand(storage)
