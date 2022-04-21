import commands.commandbase as commandbase


class ListTaskCommand(commandbase.ReportCommand):
    '''
    A command that will list tasks.
    '''
    def __init__(self, context, command_filter=None):
        super().__init__(context, command_filter)

    def get_columns(self):
        return self.context.settings.report_list_columns.split(',')


class ListTaskCommandParser(commandbase.FilterCommandParserBase):
    COMMAND_NAME = 'list'

    def __init__(self):
        super().__init__(ListTaskCommandParser.COMMAND_NAME)

    def parse(self, context, args):
        return ListTaskCommand(context)
