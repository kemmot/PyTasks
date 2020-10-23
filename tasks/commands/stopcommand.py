import commands.commandbase as commandbase
import filters.allbatchfilter as allbatchfilter
import filters.confirmfilter as confirmfilter
import entities


class StopCommand(commandbase.FilterCommandBase):
    '''
    A command that will unset the start time of existing tasks.
    '''

    def __init__(self, context, filter=None):
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
        return StopCommand(context)
    
    def get_confirm_filter(self, context):
        if context.settings.command_stop_confirm:
            return confirmfilter.ConfirmFilter('Stop')
        return None
