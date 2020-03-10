import logging


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
    def __init__(self, context, filter):
        super().__init__(context)
        self._filter = filter

    @property
    def filter(self):
        return self._filter

    def get_filtered_tasks(self):
        return self.filter.filter_items(self.context.storage.read_all())


class CommandParserBase:
    def parse(self, context, filter_factory, args):
        raise Exception('parse not implemented in {}'.format(__class__.__name__))
