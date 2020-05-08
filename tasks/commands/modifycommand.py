import commands.commandbase as commandbase
import filters.allbatchfilter as allbatchfilter
import filters.confirmfilter as confirmfilter
import entities


class ModifyCommand(commandbase.FilterCommandBase):
    '''
    A command that will modify existing tasks.
    '''

    def __init__(self, context, filter):
        super().__init__(context, filter)
        self._template_task = None

    @property
    def template_task(self):
        '''
        The task to use as a template for the modification.
        '''
        return self._template_task

    @template_task.setter
    def template_task(self, value):
        self._template_task = value

    def execute(self):
        '''
        Executes the logic of this command.
        '''
        filtered_tasks = self.get_filtered_tasks()
        for task in filtered_tasks:
            if self.template_task.name:
                task.name = self.template_task.name
            for attribute_name, attribute_value in self.template_task.attributes.items():
                task.attributes[attribute_name] = attribute_value
        self.context.storage.update(filtered_tasks)


class ModifyCommandParser(commandbase.FilterCommandParserBase):
    COMMAND_NAME = 'modify'

    def __init__(self):
        super().__init__(ModifyCommandParser.COMMAND_NAME)

    def parse(self, context, args):
        if len(args) > 2 and args[1] == ModifyCommandParser.COMMAND_NAME:
            batch_filter = allbatchfilter.AllBatchFilter()
            batch_filter.add_filter(context.filter_factory.parse(args[0]))

            if context.settings.command_modify_confirm:
                batch_filter.add_filter(confirmfilter.ConfirmFilter('Modify'))

            template_task = entities.Task()
            for arg in args[2:]:
                if ':' in arg:
                    attribute_parts = arg.split(':')
                    template_task.attributes[attribute_parts[0]] = attribute_parts[1]
                else:
                    if template_task.name:
                        template_task.name += ' '
                    template_task.name += arg

            command = ModifyCommand(context, batch_filter)
            command.template_task = template_task
        else:
            command = None
        return command
