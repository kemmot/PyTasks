
import commands.commandbase as commandbase
import entities


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
        task = self.storage.read(self.task_index)
        self.storage.delete(task)


class DoneCommandParser(commandbase.CommandParserBase):
    def parse(self, storage, args):
        if args[0] == 'done':
            if len(args) < 2:
                raise Exception('Done command requires task filter')

            filter = args[1]
            if not filter.isnumeric():
                raise Exception('Done command filter should be number')

            command = DoneCommand(storage)
            command.task_index = int(filter)
        else:
            command = None
        return command
