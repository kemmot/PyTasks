'''
A module providing task commands.
'''

import datetime
import logging
import uuid

import commands.commandbase as commandbase
import entities


class CommandFactory:
    def __init__(self, storage):
        self._parsers = {}
        self._storage = storage

    def register_known_parsers(self):
        for cla in commandbase.CommandParserBase.__subclasses__():
            self.register_parser(cla())

    def register_parser(self, parser):
        self._parsers[parser.get_name()] = parser

    def get_command(self, args):
        if not args.command in self._parsers:
            raise Exception('Command not recognised: [{}]'.format(args.command))

        parser = self._parsers[args.command]
        return parser.parse(self._storage, args)


class ListTaskCommand(commandbase.CommandBase):
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


class ListTaskCommandParser(commandbase.CommandParserBase):
    def get_name(self):
        return 'list'

    def parse(self, storage, args):
        return ListTaskCommand(storage)
