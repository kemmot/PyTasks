import commands.commandbase as commandbase


class ListTaskCommand(commandbase.CommandBase):
    '''
    A command that will list tasks.
    '''

    def execute(self):
        '''
        Executes the logic of this command.
        '''
        print('ID   Status  Description')
        print('------------------------')
        for task in self.storage.read_all():
            format_string = '{} {} {}'
            print(format_string.format( \
                    task.index, \
                    task.status, \
                    task.name))


class ListTaskCommandParser(commandbase.CommandParserBase):
    def parse(self, storage, args):
        if args[0] == 'list':
            command = ListTaskCommand(storage)
        else:
            command = None
        return command
