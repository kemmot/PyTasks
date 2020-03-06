
import commands.commandbase as commandbase
import entities
import filters.alwaysfilter as alwaysfilter
import filters.filterfactory as filterfactory


class DoneCommand(commandbase.FilterCommandBase):
    def __init__(self, context, filter):
        super().__init__(context, filter)

    def execute(self):
        tasks_to_change = self.get_filtered_tasks()
        if len(tasks_to_change) > 0:
            if len(tasks_to_change) > 1:
                message = 'Mark task(s) as done? [y/n]... {} tasks'.format(len(tasks_to_change))
            else:
                message = 'Mark task as done? [y/n]... ID: {}, name: {}'.format(tasks_to_change[0].index, tasks_to_change[0].name)

            if self._should_process(message):
                for task in tasks_to_change:
                    self.context.storage.delete(task)

    def _should_process(self, message):
        result = False
        if self.context.settings.command_done_confirm:
            print(message)
            if input().startswith('y'):
                result = True
        else:
            result = True
        return result

class DoneCommandParser(commandbase.CommandParserBase):
    def parse(self, context, filter_factory, args):
        if len(args) == 2 and args[1] == 'done':
            filter = filter_factory.parse(args[0])
            command = DoneCommand(context, filter)
        else:
            command = None
        return command
