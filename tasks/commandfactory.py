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
