
import commands.commandbase as commandbase
import entities
import filters.taskindexfilter as taskindexfilter


class DoneCommand(commandbase.CommandBase):
    def __init__(self, storage):
        super().__init__(storage)
        self._task_index = -1

    @property
    def task_index(self):
        return self._task_index

    @task_index.setter
    def task_index(self, value):
        self._task_index = value

    def execute(self):
        filter = taskindexfilter.TaskIndexFilter(self.task_index)
        tasks = self.storage.read_all()
        for task in tasks:
            if filter.is_match(task):
                self.storage.delete(task)


class DoneCommandParser(commandbase.CommandParserBase):
    def parse(self, storage, args):
        if len(args) == 2 and args[1] == 'done':
            filter = args[0]
            if not filter.isnumeric():
                raise Exception('Done command filter should be number')

            command = DoneCommand(storage)
            command.task_index = int(filter)
        else:
            command = None
        return command
