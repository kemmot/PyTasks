import datetime

import commands.commandbase as commandbase
import entities
import filters.confirmfilter as confirmfilter


class DoneCommand(commandbase.FilterCommandBase):
    def __init__(self, context, command_filter=None):
        super().__init__(context, command_filter)
        self.__message = None
    
    @property
    def message(self):
        '''
        The annotation message to add.
        '''
        return self.__message

    @message.setter
    def message(self, value):
        self.__message = value
    
    def execute_tasks(self, tasks):
        '''
        Executes the logic of this command.
        '''
        for task in tasks:
            annotation = entities.TaskAnnotation(self.message, datetime.datetime.now())
            task.annotations.append(annotation)
            task.end()
        self.context.storage.update(tasks)


class DoneCommandParser(commandbase.FilterCommandParserBase):
    COMMAND_NAME = 'done'

    def __init__(self):
        super().__init__(DoneCommandParser.COMMAND_NAME)

    def parse(self, context, args):
        command = DoneCommand(context)
        command.message = ''
        for arg in args:
            if command.message:
                command.message += ' '
            command.message += arg
        return command

    def get_confirm_filter(self, context):
        if context.settings.command_done_confirm:
            return confirmfilter.ConfirmFilter(context, 'Mark as done')
        return None
