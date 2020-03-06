import logging


class CommandBase:
    '''
    A base class providing functionality common to all commands.
    '''
    def __init__(self, storage):
        self._logger = logging.getLogger(__class__.__name__)
        self._storage = storage

    @property
    def storage(self):
        '''
        The storage to write the task to.
        '''
        return self._storage

    def execute(self):
        '''
        Executes the logic of this command.
        '''
        raise Exception('Execute not implemented in {}'.format(__class__.__name__))


class FilterCommandBase(CommandBase):
    def __init__(self, storage, filter):
        super().__init__(storage)
        self._filter = filter

    @property
    def filter(self):
        return self._filter

    def get_filtered_tasks(self):
        filtered_tasks = []
        for task in self.storage.read_all():
            if self.filter.is_match(task):
                filtered_tasks.append(task)
        return filtered_tasks


class CommandParserBase:
    def parse(self, context, filter_factory, args):
        raise Exception('parse not implemented in {}'.format(__class__.__name__))
