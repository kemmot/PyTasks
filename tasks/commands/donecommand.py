
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
    def get_name(self):
        return 'done'

    def parse(self, storage, args):
        command = DoneCommand(storage)
        command.task_index = args.filter
        return command
