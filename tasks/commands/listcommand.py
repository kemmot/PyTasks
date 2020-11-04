import commands.commandbase as commandbase
import asciitable


class ListTaskCommand(commandbase.FilterCommandBase):
    '''
    A command that will list tasks.
    '''
    def __init__(self, context, command_filter=None, table=None):
        super().__init__(context, command_filter)
        if table is None:
            table = asciitable.AsciiTable()
        self._table = table

    def execute(self):
        '''
        Executes the logic of this command.
        '''
        self._table.add_column('ID')
        self._table.add_column('Status')
        self._table.add_column('Description')
        for task in self.get_filtered_tasks():
            self._table.add_row(task.index, task.status, task.name)
        print(self._table.create_output())


class ListTaskCommandParser(commandbase.FilterCommandParserBase):
    COMMAND_NAME = 'list'

    def __init__(self):
        super().__init__(ListTaskCommandParser.COMMAND_NAME)

    def parse(self, context, args):
        return ListTaskCommand(context)
