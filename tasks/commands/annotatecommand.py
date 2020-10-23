import commands.commandbase as commandbase
import entities
import filters.allbatchfilter as allbatchfilter
import filters.confirmfilter as confirmfilter


class AnnotateCommand(commandbase.FilterCommandBase):
    def __init__(self, context, filter=None):
        super().__init__(context, filter)
        self._message = None

    @property
    def message(self):
        '''
        The annotation message to add.
        '''
        return self._message

    @message.setter
    def message(self, value):
        self._message = value

    def execute(self):
        '''
        Executes the logic of this command.
        '''
        tasks = self.get_filtered_tasks()
        for task in tasks:
            annotation = entities.TaskAnnotation(self.message)
            task.annotations.append(annotation)
            print('Task annotated: {}'.format(task.index))
        self.context.storage.update(tasks)


class AnnotateCommandParser(commandbase.FilterCommandParserBase):
    COMMAND_NAME = 'annotate'

    def __init__(self):
        super().__init__(AnnotateCommandParser.COMMAND_NAME)

    def parse(self, context, args):
        if len(args) < 1:
            raise Exception('Annotation requires at least a one word description')

        command = AnnotateCommand(context)
        command.message = ' '.join(args)
        return command
    
    def get_confirm_filter(self, context):
        if context.settings.command_annotate_confirm:
            return confirmfilter.ConfirmFilter('Annotate')
        return None
