import commands.commandbase as commandbase
import asciitable


class ListTaskCommand(commandbase.FilterCommandBase):
    '''
    A command that will list tasks.
    '''
    def __init__(self, context, command_filter=None):
        super().__init__(context, command_filter)

    def execute(self):
        self.context.storage.garbage_collect()
        super().execute()

    def execute_tasks(self, tasks):
        '''
        Executes the logic of this command.
        '''
        table = self.context.create_table()
        table.add_column('ID')
        table.add_column('Status')
        table.add_column('Description')
        for task in tasks:
            if not task.is_ended:
                table.add_row(task.index, task.status, task.name)
        print(table.create_output())


class ListTaskCommandParser(commandbase.FilterCommandParserBase):
    COMMAND_NAME = 'list'

    def __init__(self):
        super().__init__(ListTaskCommandParser.COMMAND_NAME)

    def parse(self, context, args):
        return ListTaskCommand(context)
