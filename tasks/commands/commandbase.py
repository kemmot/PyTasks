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


class CommandParserBase:
    def parse(self, storage, args):
        raise Exception('parse not implemented in {}'.format(__class__.__name__))
