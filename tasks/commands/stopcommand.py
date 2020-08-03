import commands.commandbase as commandbase
import filters.allbatchfilter as allbatchfilter
import filters.confirmfilter as confirmfilter
import entities


class StopCommand(commandbase.FilterCommandBase):
    '''
    A command that will unset the start time of existing tasks.
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
            task.stop()
        self.context.storage.update(filtered_tasks)


class StopCommandParser(commandbase.FilterCommandParserBase):
    COMMAND_NAME = 'stop'

    def __init__(self):
        super().__init__(StopCommandParser.COMMAND_NAME)

    def parse(self, context, args):
        if len(args) > 1 and args[1] == StopCommandParser.COMMAND_NAME:
            batch_filter = allbatchfilter.AllBatchFilter()
            batch_filter.add_filter(context.filter_factory.parse(args[0]))

            if context.settings.command_start_confirm:
                batch_filter.add_filter(confirmfilter.ConfirmFilter('Stop'))

            command = StopCommand(context, batch_filter)
        else:
            command = None
        return command
