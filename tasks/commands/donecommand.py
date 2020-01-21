
import commands.commandbase as commandbase
import entities
import filters.taskindexfilter as taskindexfilter


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
    def parse(self, storage, args):
        if len(args) == 2 and args[1] == 'done':
            index = args[0]
            if not index.isnumeric():
                raise Exception('Done command filter should be number')

            filter = taskindexfilter.TaskIndexFilter(int(index))
            command = DoneCommand(storage, filter)
        else:
            command = None
        return command
