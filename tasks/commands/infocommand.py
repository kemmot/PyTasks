import commands.commandbase as commandbase
import entities
import filters.allbatchfilter as allbatchfilter
import filters.alwaysfilter as alwaysfilter


class InfoCommand(commandbase.FilterCommandBase):
    def __init__(self, context, batch_filter=None):
        super().__init__(context, batch_filter)

    def execute(self):
        '''
        Executes the logic of this command.
        '''
        for task in self.get_filtered_tasks():
            print('Name        Value')
            print('ID          {}'.format(task.index))
            print('Description {}'.format(task.name))
            print('Status      {}'.format(task.status))
            print('Entered     {}'.format(task.created))
            print('UUID        {}'.format(task.id_number))

            if len(task.annotations) > 0:
                print('')
                print('Date             Modification')
                for annotation in task.annotations:
                    print('{} {}'.format(annotation.created.strftime('%Y-%m-%d %H:%M'), annotation.message))


class InfoCommandParser(commandbase.FilterCommandParserBase):
    COMMAND_NAME = 'info'

    def __init__(self):
        super().__init__(InfoCommandParser.COMMAND_NAME)

    def parse(self, context, args):
        return InfoCommand(context)
