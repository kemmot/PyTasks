import commands.commandbase as commandbase


class HelpCommand(commandbase.CommandBase):
    '''
    A command that will display command help.
    '''
    def __init__(self, context):
        super().__init__(context)

    def execute(self):
        pass


class HelpCommandParser(commandbase.CommandParserBase):
    def parse(self, context, args):
        if len(args) == 1 and args[0] == 'help':
            command = HelpCommand(context)
        else:
            command = None
        return command
