import commands.commandbase as commandbase
import datetime
import datetimeparser
import entities
import filters.confirmfilter as confirmfilter


class AnnotateCommand(commandbase.FilterCommandBase):
    def __init__(self, context, command_filter=None):
        super().__init__(context, command_filter)
        self._created = datetime.datetime.now()
        self._message = None

    @property
    def created(self):
        '''
        The annotation creation date and time to use.
        '''
        return self._created

    @created.setter
    def created(self, value):
        self._created = value
    
    @property
    def message(self):
        '''
        The annotation message to add.
        '''
        return self._message

    @message.setter
    def message(self, value):
        self._message = value

    def execute_tasks(self, tasks):
        '''
        Executes the logic of this command.
        '''
        for task in tasks:
            annotation = entities.TaskAnnotation(self.message, self.created)
            task.annotations.append(annotation)
            self.context.console.print('Task annotated: {}'.format(task.index))
        self.context.storage.update(tasks)


class AnnotateCommandParser(commandbase.FilterCommandParserBase):
    COMMAND_NAME = 'annotate'

    def __init__(self):
        super().__init__(AnnotateCommandParser.COMMAND_NAME)

    def parse(self, context, args):
        if not args:
            raise Exception('Annotation requires at least a one word description')

        command = AnnotateCommand(context)
        command.message = ''
        created_date_set = False
        for arg in args:
            arg_is_attribute = False
            if ':' in arg:
                attribute_parts = arg.split(':')
                if attribute_parts[0] == 'created':
                    if created_date_set:
                        raise Exception('Attribute already set: [{}]'.format(attribute_parts[0]))
                    else:
                        command.created = datetimeparser.DateTimeParser().parse(attribute_parts[1])
                        created_date_set = True
                    arg_is_attribute = True
            if not arg_is_attribute:
                if command.message:
                    command.message += ' '
                command.message += arg

        return command

    def get_confirm_filter(self, context):
        if context.settings.command_annotate_confirm:
            return confirmfilter.ConfirmFilter(context, 'Annotate')
        return None
