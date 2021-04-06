import commands.commandbase as commandbase
import asciitable
import console


class ListTaskCommand(commandbase.FilterCommandBase):
    '''
    A command that will list tasks.
    '''
    def __init__(self, context, command_filter=None):
        super().__init__(context, command_filter)

    def execute(self):
        super().execute()
    
    def before_execute(self):
        self.context.storage.garbage_collect()

    def execute_tasks(self, tasks):
        '''
        Executes the logic of this command.
        '''
        alt_background_colour = self.context.console.parse_backcolour(self.context.settings.table_row_alt_backcolour)
        alt_foreground_colour = self.context.console.parse_forecolour(self.context.settings.table_row_alt_forecolour)
        background_colour = self.context.console.parse_backcolour(self.context.settings.table_row_backcolour)
        foreground_colour = self.context.console.parse_forecolour(self.context.settings.table_row_forecolour)

        table = self.context.create_table()
        table.add_column('ID')
        table.add_column('Status')
        table.add_column('Description')
        for task in tasks:
            if not task.is_ended and not task.is_waiting:
                table.add_row(task.index, task.status, task.name)
        self.context.console.foreground_colour = foreground_colour
        self.context.console.background_colour = background_colour
        self.context.console.print_lines(table.create_output_lines(), alt_background_colour=alt_background_colour, alt_foregound_colour=alt_foreground_colour)


class ListTaskCommandParser(commandbase.FilterCommandParserBase):
    COMMAND_NAME = 'list'

    def __init__(self):
        super().__init__(ListTaskCommandParser.COMMAND_NAME)

    def parse(self, context, args):
        return ListTaskCommand(context)
