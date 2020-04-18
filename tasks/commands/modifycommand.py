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
            task.name = self.template_task.name
        self.context.storage.update(filtered_tasks)


class ModifyCommandParser(commandbase.CommandParserBase):
    def parse(self, context, args):
        if len(args) > 2 and args[1] == 'modify':
            batch_filter = allbatchfilter.AllBatchFilter()
            batch_filter.add_filter(context.filter_factory.parse(args[0]))

            if context.settings.command_modify_confirm:
                batch_filter.add_filter(confirmfilter.ConfirmFilter('Modify'))
            
            name = args[2:]

            template_task = entities.Task()
            template_task.name = ' '.join(name)

            command = ModifyCommand(context, batch_filter)
            command.template_task = template_task
        else:
            command = None
        return command
