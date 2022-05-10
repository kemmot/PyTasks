import logging

import asciitable
import commandline
import console
import datetimeparser
import entities


class CommandBase:
    '''
    A base class providing functionality common to all commands.
    '''
    def __init__(self, context):
        self._logger = logging.getLogger(__class__.__name__)
        self._context = context

    @property
    def context(self):
        '''
        The command context.
        '''
        return self._context
    
    def before_execute(self):
        pass

    def execute(self):
        '''
        Executes the logic of this command.
        '''
        raise Exception('Execute not implemented in {}'.format(__class__.__name__))
    

class FilterCommandBase(CommandBase):
    def __init__(self, context, command_filter=None):
        super().__init__(context)
        self._filter = command_filter

    @property
    def filter(self):
        return self._filter

    @filter.setter
    def filter(self, value):
        self._filter = value

    def execute(self):
        '''
        Executes the logic of this command.
        '''
        self.pre_filter()
        filtered_tasks = self.get_filtered_tasks()
        self.execute_tasks(filtered_tasks)
        self._logger.debug('Executed {} command on {} tasks'.format(self.__class__.__name__, len(filtered_tasks)))

    def pre_filter(self):
        # by default do nothing
        pass
    
    def execute_tasks(self, tasks):
        '''
        Executes the logic of this command against the filtered tasks.
        '''
        raise Exception('Execute(tasks) not implemented in {}'.format(__class__.__name__))

    def get_filtered_tasks(self):
        items = self.context.storage.read_all()
        filtered_items = self.filter.filter_items(items)
        self._logger.debug('Filtered {} items to {}'.format(len(items), len(filtered_items)))
        return filtered_items


class ReportCommandBase(FilterCommandBase):
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
        columns = self.get_columns()
        max_annotation_count = self.get_annotation_count()
        tasks_to_display = self.filter_tasks(tasks)
        self.sort_tasks(tasks_to_display)
        table = self.create_task_table(columns, max_annotation_count, tasks_to_display)
        self.print_table(table)

    def get_annotation_count(self):
        return 0

    def get_columns(self):
        raise Exception(f'get_columns not overridden in {self.__class__}')

    def filter_tasks(self, tasks):
        return tasks

    def sort_tasks(self, tasks):
        # do nothing by default
        pass

    def create_task_table(self, columns, max_annotation_count, tasks):
        table = asciitable.DataTable()

        description_column_index = 0
        for column in columns:
            column = column.strip()
            table.add_column(column)
            if column == 'description':
                description_column_index = len(table.columns) - 1

        for task in tasks:
            row_values = []
            for column in columns:
                column = column.strip()
                if column == 'annotation.count':
                    value = str(len(task.annotations))
                elif column == 'id':
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

            if max_annotation_count > 0:
                annotations_by_date = sorted(task.annotations, key=lambda a: a.created)
                truncated_annotations = annotations_by_date[max_annotation_count*-1:]
                for annotation in truncated_annotations:
                    row_values = []
                    for row in range(0, description_column_index):
                        row_values.append('')
                    row_values.append(f'\t{annotation.created}: {annotation.message}')
                    table.add_row(*row_values)

        return table

    def print_table(self, table):
        c = console.ConsoleFactory().get_console()
        c.foreground_colour = self.context.settings.table_row_forecolour
        c.background_colour = self.context.settings.table_row_backcolour
        c.print_table(table, self.context.settings.table_row_alt_forecolour, self.context.settings.table_row_alt_backcolour)


class CommandParserBase:
    def __init__(self, command_name):
        self._command_name = command_name
        super().__init__()

    @property
    def command_name(self):
        return self._command_name

    def parse(self, context, args):
        raise Exception('parse not implemented in {}'.format(__class__.__name__))

    def print_help(self, console):
        console.print(self.get_usage())

    def get_confirm_filter(self, context):
        return None

    def get_usage(self):
        return 'tasks {}'.format(self._command_name)

    def parse_template_task(self, args):
        template_task = entities.Task()
        for arg in args:
            if ':' in arg:
                attribute_parts = arg.split(':')
                if attribute_parts[0] in ['due', 'wait']:
                    template_task.wait_time = datetimeparser.DateTimeParser().parse(attribute_parts[1])
                else:
                    template_task.attributes[attribute_parts[0]] = attribute_parts[1]
            else:
                if template_task.name:
                    template_task.name += ' '
                template_task.name += arg
        return template_task


class FilterCommandParserBase(CommandParserBase):
    def get_usage(self):
        return 'tasks [filter] {}'.format(self.command_name)
