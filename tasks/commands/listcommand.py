import commands.commandbase as commandbase
import asciitable
import commandline
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

        columns = self.context.settings.report_list_columns.split(',')
        
        table = self.context.create_table()
        for column in columns:
            column = column.strip()
            table.add_column(column)

        for task in tasks:
            if not task.is_ended and not task.is_waiting:
                row_values = []
                for column in columns:
                    column = column.strip()
                    if column == 'id':
                        value = task.index
                    elif column == 'description':
                        value = task.name
                    elif column == 'status':
                        value = task.status
                    elif column == 'start':
                        value = task.started_time
                    elif column == 'wait':
                        value = task.wait_time
                    elif column in task.attributes:
                        value = task.attributes[column]
                    else:
                        raise commandline.ExitCodeException( \
                            commandline.ExitCodes.configuration_error, \
                            'Unknown column: [{}]'.format(column))
                    row_values.append(value)
                table.add_row(*row_values)

        self.context.console.foreground_colour = foreground_colour
        self.context.console.background_colour = background_colour
        self.context.console.print_lines(table.create_output_lines(), alt_background_colour=alt_background_colour, alt_foregound_colour=alt_foreground_colour)


class ListTaskCommandParser(commandbase.FilterCommandParserBase):
    COMMAND_NAME = 'list'

    def __init__(self):
        super().__init__(ListTaskCommandParser.COMMAND_NAME)

    def parse(self, context, args):
        return ListTaskCommand(context)
