'''
A module providing task commands.
'''

import commands.commandbase as commandbase
import commandline
import typefactory


class CommandFactory(typefactory.TypeFactory):
    def __init__(self, storage, filter_factory):
        super().__init__(commandbase.CommandParserBase)
        self._storage = storage
        self._filter_factory = filter_factory

    def get_command(self, args):
        if not args:
            exit_code = commandline.ExitCodes.no_command_specified_error
            raise commandline.ExitCodeException(exit_code=exit_code)

        command = None
        for parser in self.types:
            command = parser.parse(self._storage, args)
            if command is not None:
                break

        if command is None:
            exit_code = commandline.ExitCodes.unknown_command_error
            raise commandline.ExitCodeException(exit_code=exit_code)

        return command
