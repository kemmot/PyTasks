import commands.commandbase as commandbase
import filters.allbatchfilter as allbatchfilter
import filters.confirmfilter as confirmfilter
import entities


class StartCommand(commandbase.FilterCommandBase):
    '''
    A command that will set the start time of existing tasks.
    '''

    def __init__(self, context, filter):
        super().__init__(context, filter)
        self._template_task = None

    def execute(self):
        '''
        Executes the logic of this command.
        '''
        filtered_tasks = self.get_filtered_tasks()
        for task in filtered_tasks:
            task.start()
        self.context.storage.update(filtered_tasks)


class StartCommandParser(commandbase.FilterCommandParserBase):
    COMMAND_NAME = 'start'

    def __init__(self):
        super().__init__(StartCommandParser.COMMAND_NAME)

    def parse(self, context, args):
        if len(args) > 1 and args[1] == StartCommandParser.COMMAND_NAME:
            batch_filter = allbatchfilter.AllBatchFilter()
            batch_filter.add_filter(context.filter_factory.parse(args[0]))

            if context.settings.command_start_confirm:
                batch_filter.add_filter(confirmfilter.ConfirmFilter('Start'))

            command = StartCommand(context, batch_filter)
        else:
            command = None
        return command
