
import commands.commandbase as commandbase
import entities
import filters.alwaysfilter as alwaysfilter
import filters.filterfactory as filterfactory


class DoneCommand(commandbase.FilterCommandBase):
    def __init__(self, storage, filter):
        super().__init__(storage, filter)

    def execute(self):
        for task in self.get_filtered_tasks():
            self.storage.delete(task)


class DoneCommandParser(commandbase.CommandParserBase):
    def parse(self, context, filter_factory, args):
        if len(args) == 2 and args[1] == 'done':
            filter = filter_factory.parse(args[0])
            command = DoneCommand(context.storage, filter)
        else:
            command = None
        return command
