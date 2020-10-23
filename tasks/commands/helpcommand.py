import commands.commandbase as commandbase


class HelpCommand(commandbase.CommandBase):
    '''
    A command that will display command help.
    '''
    def __init__(self, context):
        super().__init__(context)

    def execute(self):
        sort = lambda t: t.command_name
        sorted_parsers = sorted(self.context.command_factory.types, key=sort)
        for command_parser in sorted_parsers:
            command_parser.print_help()


class HelpCommandParser(commandbase.CommandParserBase):
    COMMAND_NAME = 'help'

    def __init__(self):
        super().__init__(HelpCommandParser.COMMAND_NAME)

    def parse(self, context, args):
        return HelpCommand(context)
