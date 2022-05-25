import commands.commandbase as commandbase
import entities


class ColumnsCommand(commandbase.FilterCommandBase):
    def __init__(self, context, command_filter=None):
        super().__init__(context, command_filter)

    def execute_tasks(self, tasks):
        '''
        Executes the logic of this command.
        '''
        alt_background_colour = self.context.console.parse_backcolour(self.context.settings.table_row_alt_backcolour)
        alt_foreground_colour = self.context.console.parse_forecolour(self.context.settings.table_row_alt_forecolour)
        background_colour = self.context.console.parse_backcolour(self.context.settings.table_row_backcolour)
        foreground_colour = self.context.console.parse_forecolour(self.context.settings.table_row_forecolour)

        table = self.context.create_table()
        table.add_column('Columns')
        table.add_column('Type')
        table.add_column('Modifiable')
        table.add_column('Supported Formats')
        table.add_column('Example')

        custom_attribute_values = {}
        attributes_names = entities.TaskAttributeName.get_names()
        for task in tasks:
            for attribute_name, attribute_value in task.attributes.items():
                if not attribute_name in custom_attribute_values:
                    attributes_names.append(attribute_name)
                    now_custom_attribute_values = []
                    custom_attribute_values[attribute_name] = now_custom_attribute_values
                else:
                    now_custom_attribute_values = custom_attribute_values[attribute_name]
                if not attribute_value in now_custom_attribute_values:
                    now_custom_attribute_values.append(attribute_value)

        attributes_names.sort()

        for attribute_name in attributes_names:
            if attribute_name == entities.TaskAttributeName.DESCRIPTION:
                for row in self._get_rows_for_desc_attribute():
                    table.add_row(*row)
            elif attribute_name == entities.TaskAttributeName.END:
                for row in self._get_rows_for_date_attribute(entities.TaskAttributeName.END, modifiable=True):
                    table.add_row(*row)
            elif attribute_name == entities.TaskAttributeName.ENTRY:
                for row in self._get_rows_for_date_attribute(entities.TaskAttributeName.ENTRY, modifiable=True):
                    table.add_row(*row)
            elif attribute_name == entities.TaskAttributeName.ID:
                for row in self._get_rows_for_numeric_attribute(entities.TaskAttributeName.ID, modifiable=False):
                    table.add_row(*row)
            elif attribute_name == entities.TaskAttributeName.START:
                for row in self._get_rows_for_date_attribute(entities.TaskAttributeName.START, modifiable=False):
                    table.add_row(*row)
            elif attribute_name == entities.TaskAttributeName.STATUS:
                for row in self._get_rows_for_status_attribute():
                    table.add_row(*row)
            elif attribute_name == entities.TaskAttributeName.WAIT:
                for row in self._get_rows_for_date_attribute(entities.TaskAttributeName.WAIT, modifiable=False):
                    table.add_row(*row)
            else:
                for row in sorted(self._get_rows_for_custom_attribute(attribute_name, custom_attribute_values[attribute_name])):
                    table.add_row(*row)

        self.context.console.foreground_colour = foreground_colour
        self.context.console.background_colour = background_colour
        self.context.console.print_lines(
            table.create_output_lines(), \
            alt_background_colour=alt_background_colour, \
            alt_foregound_colour=alt_foreground_colour)
        self.context.console.print_lines(['', '* Means default format, and therefore optional.'])

    def _get_rows_for_custom_attribute(self, name, values):
        rows = []
        rows.append(self._get_row(name, 'string', True, '', ''))
        for value in values:
            rows.append(self._get_additional_format_row('', value))
        return rows

    def _get_rows_for_desc_attribute(self):
        rows = []
        rows.append(self._get_row(entities.TaskAttributeName.DESCRIPTION, 'string', True, 'desc', 'Move your clothes down on to the lower peg'))
        return rows

    def _get_rows_for_date_attribute(self, name, modifiable):
        rows = []
        rows.append(self._get_row(name, 'date', modifiable, 'formatted', '2021-04-17'))
        rows.append(self._get_additional_format_row('relative', '-4d'))
        return rows

    def _get_rows_for_numeric_attribute(self, name, modifiable):
        rows = []
        rows.append(self._get_row(name, 'numeric', modifiable, 'number*', '123'))
        return rows

    def _get_rows_for_status_attribute(self):
        rows = []
        rows.append(self._get_row(entities.TaskAttributeName.STATUS, 'string', True, 'long*', 'Pending'))
        rows.append(self._get_additional_format_row('short', 'P'))
        return rows

    def _get_additional_format_row(self, format, example):
        return self._get_row('', '', None, format, example)

    def _get_row(self, name, type, modifiable, format, example):
        row_values = []
        row_values.append(name)
        row_values.append(type)
        row_values.append('' if not modifiable else ('Modifiable' if modifiable else 'Read Only'))
        row_values.append(format)
        row_values.append(example)
        return row_values


class ColumnsCommandParser(commandbase.FilterCommandParserBase):
    COMMAND_NAME = 'columns'

    def __init__(self):
        super().__init__(ColumnsCommandParser.COMMAND_NAME)

    def parse(self, context, args):
        return ColumnsCommand(context)

    def get_confirm_filter(self, context):
        return None
