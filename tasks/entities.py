'''
Module for task related entity classes.
'''

class Task:
    '''
    A class for encapsulating task details.
    '''
    def __init__(self):
        self._name = ''

    @property
    def name(self):
        '''
        The name of the task.
        '''
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
