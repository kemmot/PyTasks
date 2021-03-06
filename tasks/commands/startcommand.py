import commands.commandbase as commandbase
import filters.confirmfilter as confirmfilter


class StartCommand(commandbase.FilterCommandBase):
    '''
    A command that will set the start time of existing tasks.
    '''

    def __init__(self, context, command_filter=None):
        super().__init__(context, command_filter)
        self._template_task = None

    def execute_tasks(self, tasks):
        '''
        Executes the logic of this command.
        '''
        for task in tasks:
            task.start()
        self.context.storage.update(tasks)


class StartCommandParser(commandbase.FilterCommandParserBase):
    COMMAND_NAME = 'start'

    def __init__(self):
        super().__init__(StartCommandParser.COMMAND_NAME)

    def parse(self, context, args):
        return StartCommand(context)

    def get_confirm_filter(self, context):
        if context.settings.command_start_confirm:
            return confirmfilter.ConfirmFilter(context, 'Start')
        return None
