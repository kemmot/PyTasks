import commands.commandbase as commandbase
import entities
import filters.allbatchfilter as allbatchfilter
import filters.confirmfilter as confirmfilter


class DoneCommand(commandbase.FilterCommandBase):
    def __init__(self, context, filter):
        super().__init__(context, filter)

    def execute(self):
        for task in self.get_filtered_tasks():
            self.context.storage.delete(task)


class DoneCommandParser(commandbase.CommandParserBase):
    def parse(self, context, filter_factory, args):
        if len(args) == 2 and args[1] == 'done':
            batch_filter = allbatchfilter.AllBatchFilter()
            batch_filter.add_filter(filter_factory.parse(args[0]))

            if context.settings.command_done_confirm:
                batch_filter.add_filter(confirmfilter.ConfirmFilter('Mark as done'))

            command = DoneCommand(context, batch_filter)
        else:
            command = None
        return command
