import commands.commandbase as commandbase
import filters.confirmfilter as confirmfilter


class DoneCommand(commandbase.FilterCommandBase):
    def execute_tasks(self, tasks):
        for task in tasks:
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
