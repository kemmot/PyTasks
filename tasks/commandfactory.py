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
        self._parsers = []
        self._storage = storage

    def register_known_parsers(self):
        for cla in commandbase.CommandParserBase.__subclasses__():
            self.register_parser(cla())

    def register_parser(self, parser):
        self._parsers.append(parser)

    def get_command(self, args):
        for parser in self._parsers:
            command = parser.parse(self._storage, args)
            if command != None:
                break

        if command == None:
            raise Exception('Command not recognised: [{}]'.format(args.command))

        return command
