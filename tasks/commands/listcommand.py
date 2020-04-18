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


class ListTaskCommandParser(commandbase.CommandParserBase):
    def parse(self, context, args):
        if len(args) == 1 and args[0] == 'list':
            filter = alwaysfilter.AlwaysFilter()
            command = ListTaskCommand(context, filter)
        elif len(args) == 2 and args[1] == 'list':
            filter = context.filter_factory.parse(args[0])
            command = ListTaskCommand(context, filter)
        else:
            command = None
        return command
