'''
A module providing task commands.
'''

import datetime
import logging
import uuid

import commandline
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
        if len(args) == 0:
            raise commandline.ExitCodeException(exit_code=commandline.ExitCodes.no_command_specified_error)

        command = None
        for parser in self._parsers:
            command = parser.parse(self._storage, args)
            if command != None:
                break

        if command == None:
            raise commandline.ExitCodeException(exit_code=commandline.ExitCodes.unknown_command_error)

        return command
