
import commands.commandbase as commandbase
import entities
import filters.alwaysfilter as alwaysfilter
import filters.filterfactory as filterfactory


class DoneCommand(commandbase.CommandBase):
    def __init__(self, storage, filter):
        super().__init__(storage)
        self._filter = filter
    
    @property
    def filter(self):
        return self._filter

    def execute(self):
        tasks = self.storage.read_all()
        for task in tasks:
            if self._filter.is_match(task):
                self.storage.delete(task)


class DoneCommandParser(commandbase.CommandParserBase):
    def parse(self, storage, filter_factory, args):
        if len(args) == 2 and args[1] == 'done':
            filter = filter_factory.parse(args[0])
            command = DoneCommand(storage, filter)
        else:
            command = None
        return command
