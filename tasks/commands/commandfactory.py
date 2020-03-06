'''
A module providing task commands.
'''

import commands.commandbase as commandbase
import commandline
import typefactory


class CommandFactory(typefactory.TypeFactory):
    def __init__(self, command_context, filter_factory):
        super().__init__(commandbase.CommandParserBase)
        self._command_context = command_context
        self._filter_factory = filter_factory

    def get_command(self, args):
        if not args:
            args = self._command_context.settings.command_default.split()

        if not args:
            exit_code = commandline.ExitCodes.no_command_specified_error
            raise commandline.ExitCodeException(exit_code=exit_code)

        command = None
        for parser in self.types:
            command = parser.parse(self._command_context, self._filter_factory, args)
            if command is not None:
                break

        if command is None:
            exit_code = commandline.ExitCodes.unknown_command_error
            raise commandline.ExitCodeException(exit_code=exit_code)

        return command
