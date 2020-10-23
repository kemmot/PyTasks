import commands.commandbase as commandbase
import entities

import logging


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    CBLACK  = '\33[30m'
    CRED    = '\33[31m'
    CGREEN  = '\33[32m'
    CYELLOW = '\33[33m'
    CBLUE   = '\33[34m'
    CVIOLET = '\33[35m'
    CBEIGE  = '\33[36m'
    CWHITE  = '\33[37m'


class Console:
    pass

class Shell:
    def __init__(self, commnd_callback):
        self._exit_command = 'exit'
        self._prompt = '> '
        self._commnd_callback = commnd_callback
        self._logger = logging.getLogger(__class__.__name__)
    
    @property
    def exit_command(self):
        return self._exit_command
    
    @exit_command.setter
    def exit_command(self, value):
        self._exit_command = value
    
    @property
    def prompt(self):
        return self._prompt
    
    @prompt.setter
    def prompt(self, value):
        self._prompt = value
    
    def enter(self):
        print('Entered shell, enter "{}" to exit'.format(self.exit_command))
        while True:
            command_string = input(bcolors.CGREEN + self.prompt + bcolors.CWHITE)
            if command_string == self.exit_command:
                break

            try:
                self._commnd_callback(command_string)
            except Exception as ex:
                self._logger.error(str(ex), exc_info=True)


class ShellCommand(commandbase.CommandBase):
    '''
    A command that will enter an interactive shell supporting task commands.
    '''

    def __init__(self, context):
        super().__init__(context)
        self._template_task = None

    def execute(self):
        '''
        Executes the logic of this command.
        '''

        shell = Shell(self.handle_command)
        shell.prompt = 'task> '
        shell.enter()
    
    def handle_command(self, command_string):
        command_args = command_string.split(' ')
        COMMAND = self.context.command_factory.get_command(command_args)
        COMMAND.execute()


class ShellCommandParser(commandbase.CommandParserBase):
    COMMAND_NAME = 'shell'

    def __init__(self):
        super().__init__(ShellCommandParser.COMMAND_NAME)

    def parse(self, context, args):
        if len(args) > 0 and args[0] == ShellCommandParser.COMMAND_NAME:
            command = ShellCommand(context)
        else:
            command = None
        return command
