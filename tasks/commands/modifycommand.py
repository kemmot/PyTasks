import commands.commandbase as commandbase
import entities
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

    def before_execute(self):
        self._print_changes()

    def _print_changes(self):
        if self.context.settings.command_modify_summary:
            if self.template_task.name:
                self._print_change(entities.TaskAttributeName.DESCRIPTION, self.template_task.name)
            
            if self.template_task.wait_time:
                self._print_change(entities.TaskAttributeName.WAIT, self.template_task.wait_time)
            
            for attribute_name, attribute_value in self.template_task.attributes.items():
                self._print_change(attribute_name, attribute_value)
            
            for tag_name in self.template_task.tags:
                self.context.console.print(f'Adding tag: {tag_name}')
            
            for tag_name in self.template_task.tags_to_remove:
                self.context.console.print(f'Removing tag: {tag_name}')
            
            for dependency_index in self.template_task.dependency_ids:
                if dependency_index > 0:
                    self.context.console.print(f'Add dependency: {dependency_index}')
                else:
                    self.context.console.print(f'Remove dependency: {dependency_index * -1}')

    def _print_change(self, modified_attribute, new_value):
        self.context.console.print(f'Changing {modified_attribute} to {new_value}')

    def execute_tasks(self, tasks):
        '''
        Executes the logic of this command.
        '''
        tasks_by_index = {}
        for task in self.context.storage.read_all():
            tasks_by_index[task.index] = task
        
        for task in tasks:
            if self.template_task.name:
                task.name = self.template_task.name
            if self.template_task.wait_time:
                task.wait_time = self.template_task.wait_time
            if self.template_task.tags:
                for tag_name in self.template_task.tags:
                    task.add_tag(tag_name)
            if self.template_task.tags_to_remove:
                for tag_name in self.template_task.tags_to_remove:
                    task.remove_tag(tag_name)
            for attribute_name, attribute_value in self.template_task.attributes.items():
                task.attributes[attribute_name] = attribute_value
            self.__alter_dependencies(task, tasks_by_index)

        self.context.storage.update(tasks)
        if self.context.settings.command_modify_summary:
            self.context.console.print(f'{len(tasks)} tasks modified')
    
    def __alter_dependencies(self, task, tasks_by_index):
        for dependency_index in self.template_task.dependency_ids:
            if dependency_index > 0:
                is_adding = True
            else:
                is_adding = False
                dependency_index *= -1
            if dependency_index in tasks_by_index:
                dependency_id = tasks_by_index[dependency_index].id_number
                if is_adding:
                    if not dependency_id in task.dependency_ids:
                        task.dependency_ids.append(dependency_id)
                else:
                    if dependency_id in task.dependency_ids:
                        task.dependency_ids.remove(dependency_id)
            else:
                self._logger.warn('Dependency index not found: {}'.format(dependency_index))


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
