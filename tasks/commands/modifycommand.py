import commands.commandbase as commandbase
import filters.confirmfilter as confirmfilter


class ModifyCommand(commandbase.FilterCommandBase):
    '''
    A command that will modify existing tasks.
    '''

    def __init__(self, context, command_filter=None):
        super().__init__(context, command_filter)
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

    def execute_tasks(self, tasks):
        '''
        Executes the logic of this command.
        '''
        modified_attributes = {}
        for task in tasks:
            if self.template_task.name:
                task.name = self.template_task.name
                if not 'name' in modified_attributes:
                    modified_attributes['name'] = self.template_task.name
            if self.template_task.wait_time:
                task.wait_time = self.template_task.wait_time
                if not 'wait' in modified_attributes:
                    modified_attributes['wait'] = self.template_task.wait_time
            for attribute_name, attribute_value in self.template_task.attributes.items():
                task.attributes[attribute_name] = attribute_value
                if not attribute_name in modified_attributes:
                    modified_attributes[attribute_name] = attribute_value
        self.context.storage.update(tasks)
        if self.context.settings.command_modify_summary:
            for modified_attribute in modified_attributes:
                self.context.console.print(f'Changed {modified_attribute} to {modified_attributes[modified_attribute]}')
            self.context.console.print(f'{len(tasks)} tasks modified')


class ModifyCommandParser(commandbase.FilterCommandParserBase):
    COMMAND_NAME = 'modify'

    def __init__(self):
        super().__init__(ModifyCommandParser.COMMAND_NAME)

    def parse(self, context, args):
        command = ModifyCommand(context)
        command.template_task = self.parse_template_task(args)
        return command

    def get_confirm_filter(self, context):
        if context.settings.command_modify_confirm:
            return confirmfilter.ConfirmFilter(context, 'Modify')
        return None

    def get_usage(self):
        return super().get_usage() + ' [attribute:value]'
