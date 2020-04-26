import commands.commandbase as commandbase
import filters.alwaysfilter as alwaysfilter
import filters.filterfactory as filterfactory


class ListTaskCommand(commandbase.FilterCommandBase):
    '''
    A command that will list tasks.
    '''

    def __init__(self, context, filter):
        super().__init__(context, filter)
        
    def execute(self):
        '''
        Executes the logic of this command.
        '''
        print('ID   Status  Description')
        print('------------------------')
        for task in self.get_filtered_tasks():
            format_string = '{} {} {}'
            print(format_string.format( \
                    task.index, \
                    task.status, \
                    task.name))


class ListTaskCommandParser(commandbase.FilterCommandParserBase):
    COMMAND_NAME = 'list'

    def __init__(self):
        super().__init__(ListTaskCommandParser.COMMAND_NAME)

    def parse(self, context, args):
        if len(args) == 1 and args[0] == ListTaskCommandParser.COMMAND_NAME:
            filter = alwaysfilter.AlwaysFilter()
            command = ListTaskCommand(context, filter)
        elif len(args) == 2 and args[1] == ListTaskCommandParser.COMMAND_NAME:
            filter = context.filter_factory.parse(args[0])
            command = ListTaskCommand(context, filter)
        else:
            command = None
        return command
