'''
A module providing task commands.
'''

import logging

class AddTaskCommand:
    '''
    A command that will add a task.
    '''
    def __init__(self):
        self._logger = logging.getLogger(__class__.__name__)
        self._filename = ''
        self._name = ''

    @property
    def filename(self):
        '''
        The filename to write the task to.
        '''
        return self._filename

    @filename.setter
    def filename(self, value):
        self._filename = value

    @property
    def name(self):
        '''
        The name of the task to add.
        '''
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    def execute(self):
        '''
        Executes the logic of this command.
        '''
        with open(self.filename, 'a+') as file:
            file.write(self._format_task() + '\n')
        self._logger.info('Created task')

    def _format_task(self):
        output = '[description:"{}"]'.format(self.name)
        return output
