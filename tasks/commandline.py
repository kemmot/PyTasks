'''
Module used for parsing command line arguments.
'''


class ExitCodes:
    success = 0
    command_line_argument_error = 1
    no_command_specified_error = 2
    unknown_command_error = 3
    configuration_error = 4
    unknown_error = 99

    @staticmethod
    def get_description(value):
        if value == ExitCodes.success:
            description = 'Success'
        elif value == ExitCodes.command_line_argument_error:
            description = 'Command line argument error'
        elif value == ExitCodes.no_command_specified_error:
            description = 'No command specified'
        elif value == ExitCodes.unknown_command_error:
            description = 'Unknown command'
        elif value == ExitCodes.configuration_error:
            description = 'Configuration error'
        else:
            description = 'Unknown Error'
        return description


class ExitCodeException(Exception):
    def __init__(self, exit_code, message='',):
        if message == '':
            message = ExitCodes.get_description(exit_code)
        Exception.__init__(self, message)
        self._exit_code = exit_code

    @property
    def exit_code(self):
        return self._exit_code
