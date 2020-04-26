import commands.commandbase as commandbase


class HelpCommand(commandbase.CommandBase):
    '''
    A command that will display command help.
    '''
    def __init__(self, context):
        super().__init__(context)

    def execute(self):
        for command_parser in self.context.command_factory.types:
            command_parser.print_help()


class HelpCommandParser(commandbase.CommandParserBase):
    COMMAND_NAME = 'help'

    def __init__(self):
        super().__init__(HelpCommandParser.COMMAND_NAME)

    def parse(self, context, args):
        if len(args) == 1 and args[0] == HelpCommandParser.COMMAND_NAME:
            command = HelpCommand(context)
        else:
            command = None
        return command
