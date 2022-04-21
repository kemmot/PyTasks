import functools

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

        tasks_to_display = [t for t in tasks if not t.is_ended and not t.is_waiting]
        task_sort_by_key = functools.cmp_to_key(ListTaskCommand.__task_sort)
        tasks_to_display.sort(key=task_sort_by_key)
        for task in tasks_to_display:
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
    
    def __task_sort(a, b):
        result = ListTaskCommand.__task_sort_by_due(a, b)
        if result == 0:
            result = ListTaskCommand.__task_sort_by_priority(a, b)
            
        return result
    
    def __task_sort_by_due(a, b):
        key = 'due'
        if key in a.attributes:
            if key in b.attributes:
                a_value = a.attributes[key]
                b_value = b.attributes[key]
                if a_value < b_value:
                    result = 1
                elif a_value > b_value:
                    result = -1
                else:
                    result = 0
            else:
                result = -1
        elif key in b.attributes:
            result = 1
        else:
            result = 0
            
        return result
    
    def __task_sort_by_priority(a, b):
        key = 'priority'
        if key in a.attributes:
            if key in b.attributes:
                a_value = a.attributes[key]
                b_value = b.attributes[key]
                if a_value < b_value:
                    result = 1
                elif a_value > b_value:
                    result = -1
                else:
                    result = 0
            else:
                result = -1
        elif key in b.attributes:
            result = 1
        else:
            result = 0
            
        return result


class ListTaskCommandParser(commandbase.FilterCommandParserBase):
    COMMAND_NAME = 'list'

    def __init__(self):
        super().__init__(ListTaskCommandParser.COMMAND_NAME)

    def parse(self, context, args):
        return ListTaskCommand(context)
