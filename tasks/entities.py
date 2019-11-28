'''
Module for task related entity classes.
'''

class Task:
    '''
    A class for encapsulating task details.
    '''
    def __init__(self):
        self._id = ''
        self._name = ''
        self._status = ''

    @property
    def id(self):
        '''
        The id of the task.
        '''
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def name(self):
        '''
        The name of the task.
        '''
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def status(self):
        '''
        The status of the task.
        '''
        return self._status

    @status.setter
    def status(self, value):
        self._status = value
