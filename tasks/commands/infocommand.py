import commands.commandbase as commandbase


class InfoCommand(commandbase.FilterCommandBase):
    def __init__(self, context, batch_filter=None):
        super().__init__(context, batch_filter)

    def execute_tasks(self, tasks):
        '''
        Executes the logic of this command.
        '''
        for task in tasks:
            self.context.console.print('Name        Value')
            self.context.console.print('ID          {}'.format(task.index))
            self.context.console.print('Description {}'.format(task.name))
            self.context.console.print('Status      {}'.format(task.status))
            self.context.console.print('Entered     {}'.format(task.created_time))
            self.context.console.print('UUID        {}'.format(task.id_number))

            if task.annotations:
                self.context.console.print('')
                self.context.console.print('Date             Modification')
                for annotation in task.annotations:
                    date = annotation.created.strftime('%Y-%m-%d %H:%M')
                    self.context.console.print('{} {}'.format(date, annotation.message))


class InfoCommandParser(commandbase.FilterCommandParserBase):
    COMMAND_NAME = 'info'

    def __init__(self):
        super().__init__(InfoCommandParser.COMMAND_NAME)

    def parse(self, context, args):
        return InfoCommand(context)
