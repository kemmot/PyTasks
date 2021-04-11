import commands.commandbase as commandbase
import filters.confirmfilter as confirmfilter


class StopCommand(commandbase.FilterCommandBase):
    '''
    A command that will unset the start time of existing tasks.
    '''

    def __init__(self, context, command_filter=None):
        super().__init__(context, command_filter)
        self._template_task = None

    def execute_tasks(self, tasks):
        '''
        Executes the logic of this command.
        '''
        for task in tasks:
            task.stop()
        self.context.storage.update(tasks)


class StopCommandParser(commandbase.FilterCommandParserBase):
    COMMAND_NAME = 'stop'

    def __init__(self):
        super().__init__(StopCommandParser.COMMAND_NAME)

    def parse(self, context, args):
        return StopCommand(context)

    def get_confirm_filter(self, context):
        if context.settings.command_stop_confirm:
            return confirmfilter.ConfirmFilter(context, 'Stop')
        return None
