import commands.commandbase as commandbase

import asciitable
import console


class TagsCommand(commandbase.FilterCommandBase):
    '''
    A command that will list tags.
    '''
    def __init__(self, context, command_filter=None):
        super().__init__(context, command_filter)
    
    def execute_tasks(self, tasks):
        '''
        Executes the logic of this command.
        '''
        tag_counts = {}
        for task in tasks:
            for tag in task.tags:
                if tag in tag_counts:
                    count = tag_counts[tag] + 1
                else:
                    count = 1
                tag_counts[tag] = count
        
        table = asciitable.DataTable()
        table.add_column('Tag')
        table.add_column('Tasks')
        for tag in sorted(tag_counts.keys()):
            table.add_row(tag, str(tag_counts[tag]))
        self.print_table(table)

    def print_table(self, table):
        c = console.ConsoleFactory().get_console()
        c.foreground_colour = self.context.settings.table_row_forecolour
        c.background_colour = self.context.settings.table_row_backcolour
        c.print_table(table, self.context.settings.table_row_alt_forecolour, self.context.settings.table_row_alt_backcolour)


class TagsCommandParser(commandbase.FilterCommandParserBase):
    COMMAND_NAME = 'tags'

    def __init__(self):
        super().__init__(TagsCommandParser.COMMAND_NAME)

    def parse(self, context, args):
        return TagsCommand(context)
