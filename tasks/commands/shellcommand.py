import logging

import commands.commandbase as commandbase


class Shell:
    def __init__(self, command_callback):
        self._exit_command = 'exit'
        self._prompt = '> '
        self._logger = logging.getLogger(__class__.__name__)
        if not command_callback:
            raise ValueError('command_callback cannot be None')
        self._command_callback = command_callback

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
            command_string = input(self.prompt)
            if command_string == self.exit_command:
                break

            try:
                self._command_callback(command_string)
            except Exception as ex:
                self._logger.error(str(ex), exc_info=True)


class ShellCommand(commandbase.CommandBase):
    '''
    A command that will enter an interactive shell supporting task commands.
    '''

    def __init__(self, context, shell=None):
        '''
        shell parameter intended for test use only.
        '''
        super().__init__(context)
        self._template_task = None
        if shell:
            self._shell = shell
        else:
            self._shell = Shell(self.handle_command)
        self._shell.prompt = 'task> '

    def execute(self):
        '''
        Executes the logic of this command.
        '''
        self._shell.enter()

    def handle_command(self, command_string):
        command_args = command_string.split(' ')
        command = self.context.command_factory.get_command(command_args)
        command.execute()


class ShellCommandParser(commandbase.CommandParserBase):
    COMMAND_NAME = 'shell'

    def __init__(self):
        super().__init__(ShellCommandParser.COMMAND_NAME)

    def parse(self, context, args):
        if args and args[0] == ShellCommandParser.COMMAND_NAME:
            command = ShellCommand(context)
        else:
            command = None
        return command
