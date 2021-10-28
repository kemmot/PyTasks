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
        table = asciitable.DataTable()

        columns = self.context.settings.report_list_columns.split(',')
        for column in columns:
            column = column.strip()
            table.add_column(column)

        for task in tasks:
            if not task.is_ended and not task.is_waiting:
                row_values = []
                for column in columns:
                    column = column.strip()
                    if column == 'id':
                        value = str(task.index)
                    elif column == 'description':
                        value = task.name
                    elif column == 'status':
                        value = task.status
                    elif column == 'start':
                        value = str(task.started_time)
                    elif column == 'wait':
                        value = str(task.wait_time)
                    elif column in task.attributes:
                        value = str(task.attributes[column])
                    else:
                        value = ''
                    row_values.append(value)
                table.add_row(*row_values)
        
        c = console.ConsoleFactory().get_console()
        c.foreground_colour = self.context.settings.table_row_forecolour
        c.background_colour = self.context.settings.table_row_backcolour
        c.print_table(table, self.context.settings.table_row_alt_forecolour, self.context.settings.table_row_alt_backcolour)


class ListTaskCommandParser(commandbase.FilterCommandParserBase):
    COMMAND_NAME = 'list'

    def __init__(self):
        super().__init__(ListTaskCommandParser.COMMAND_NAME)

    def parse(self, context, args):
        return ListTaskCommand(context)
