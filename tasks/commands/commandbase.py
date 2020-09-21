import logging
import abc


class CommandBase:
    '''
    A base class providing functionality common to all commands.
    '''
    def __init__(self, context):
        self._logger = logging.getLogger(__class__.__name__)
        self._context = context

    @property
    def context(self):
        '''
        The command context.
        '''
        return self._context

    def execute(self):
        '''
        Executes the logic of this command.
        '''
        raise Exception('Execute not implemented in {}'.format(__class__.__name__))


class FilterCommandBase(CommandBase):
    def __init__(self, context, filter=None):
        super().__init__(context)
        self._filter = filter

    @property
    def filter(self):
        return self._filter
    
    @filter.setter
    def filter(self, value):
        self._filter = value

    def get_filtered_tasks(self):
        return self.filter.filter_items(self.context.storage.read_all())


class CommandParserBase:
    def __init__(self, command_name):
        self._command_name = command_name
        super().__init__()
    
    @property
    def command_name(self):
        return self._command_name

    def parse(self, context, args):
        raise Exception('parse not implemented in {}'.format(__class__.__name__))

    def print_help(self):
        print(self.get_usage())

    def get_confirm_filter(self, context):
        return None

    def get_usage(self):
        return 'tasks {}'.format(self._command_name)


class FilterCommandParserBase(CommandParserBase):
    def __init__(self, command_name):
        super().__init__(command_name)

    def get_usage(self):
        return 'tasks [filter] {}'.format(self.command_name)
