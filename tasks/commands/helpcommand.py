import commands.commandbase as commandbase


class HelpCommand(commandbase.CommandBase):
    '''
    A command that will display command help.
    '''
    def execute(self):
        sort = lambda t: t.command_name
        sorted_parser_names = sorted(self.context.command_factory.types.keys())
        for command_parser_name in sorted_parser_names:
            command_parser = self.context.command_factory.types[command_parser_name]
            command_parser.print_help(self.context.console)


class HelpCommandParser(commandbase.CommandParserBase):
    COMMAND_NAME = 'help'

    def __init__(self):
        super().__init__(HelpCommandParser.COMMAND_NAME)

    def parse(self, context, args):
        return HelpCommand(context)
