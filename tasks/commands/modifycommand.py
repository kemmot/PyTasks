import commands.commandbase as commandbase
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
    def parse(self, context, filter_factory, args):
        if len(args) > 2 and args[1] == 'modify':
            filter = filter_factory.parse(args[0])
            
            name = args[2:]

            template_task = entities.Task()
            template_task.name = ' '.join(name)

            command = ModifyCommand(context, filter)
            command.template_task = template_task
        else:
            command = None
        return command
