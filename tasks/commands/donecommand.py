import commands.commandbase as commandbase
import entities
import filters.confirmfilter as confirmfilter


class DoneCommand(commandbase.FilterCommandBase):
    def __init__(self, context, filter=None):
        super().__init__(context, filter)

    def execute(self):
        for task in self.get_filtered_tasks():
            self.context.storage.delete(task)


class DoneCommandParser(commandbase.FilterCommandParserBase):
    COMMAND_NAME = 'done'

    def __init__(self):
        super().__init__(DoneCommandParser.COMMAND_NAME)

    def parse(self, context, args):
        return DoneCommand(context)
    
    def get_confirm_filter(self, context):
        if context.settings.command_done_confirm:
            return confirmfilter.ConfirmFilter('Mark as done')
        return None
