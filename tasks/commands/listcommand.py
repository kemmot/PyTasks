import commands.commandbase as commandbase
import filters.alwaysfilter as alwaysfilter
import filters.taskindexfilter as taskindexfilter


class ListTaskCommand(commandbase.CommandBase):
    '''
    A command that will list tasks.
    '''

    def __init__(self, storage, filter):
        super().__init__(storage)
        self._filter = filter

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
    def parse(self, storage, args):
        if len(args) == 1 and args[0] == 'list':
            filter = alwaysfilter.AlwaysFilter()
            command = ListTaskCommand(storage, filter)
        elif len(args) == 2 and args[1] == 'list':
            index = args[0]
            if not index.isnumeric():
                raise Exception('List command filter should be number')

            filter = taskindexfilter.TaskIndexFilter(int(index))
            command = ListTaskCommand(storage, filter)
        else:
            command = None
        return command
