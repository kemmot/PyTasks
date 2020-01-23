import commands.commandbase as commandbase
import filters.alwaysfilter as alwaysfilter
import filters.filterfactory as filterfactory


class ListTaskCommand(commandbase.CommandBase):
    '''
    A command that will list tasks.
    '''

    def __init__(self, storage, filter):
        super().__init__(storage)
        self._filter = filter

    @property
    def filter(self):
        return self._filter
        
    def execute(self):
        '''
        Executes the logic of this command.
        '''
        print('ID   Status  Description')
        print('------------------------')
        for task in self.storage.read_all():
            if self._filter.is_match(task):
                format_string = '{} {} {}'
                print(format_string.format( \
                        task.index, \
                        task.status, \
                        task.name))


class ListTaskCommandParser(commandbase.CommandParserBase):
    def parse(self, storage, filter_factory, args):
        if len(args) == 1 and args[0] == 'list':
            filter = alwaysfilter.AlwaysFilter()
            command = ListTaskCommand(storage, filter)
        elif len(args) == 2 and args[1] == 'list':
            filter = filter_factory.parse(args[0])
            command = ListTaskCommand(storage, filter)
        else:
            command = None
        return command
