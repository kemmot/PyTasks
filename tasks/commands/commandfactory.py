'''
A module providing task commands.
'''

import commands.commandbase as commandbase
import commandline


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
        if not args:
            exit_code = commandline.ExitCodes.no_command_specified_error
            raise commandline.ExitCodeException(exit_code=exit_code)

        command = None
        for parser in self._parsers:
            command = parser.parse(self._storage, args)
            if command is not None:
                break

        if command is None:
            exit_code = commandline.ExitCodes.unknown_command_error
            raise commandline.ExitCodeException(exit_code=exit_code)

        return command
