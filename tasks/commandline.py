'''
Module used for parsing command line arguments.
'''


class ExitCodes:
    success = 0
    command_line_argument_error = 1
    unknown_error = 99

    @staticmethod
    def get_description(value):
        if value == ExitCodes.success:
            description = 'Success'
        elif value == ExitCodes.command_line_argument_error:
            description = 'Command Line Argument Error'
        else:
            description = 'Unknown Error'
        return description


class ExitCodeException(Exception):
    def __init__(self, message, exit_code=ExitCodes.unknown_error):
        Exception.__init__(self, message)
        self._exit_code = exit_code

    @property
    def exit_code(self):
        return self._exit_code
