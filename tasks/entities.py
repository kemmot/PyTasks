'''
Module for task related entity classes.
'''


class Task:
    '''
    A class for encapsulating task details.
    '''
    def __init__(self):
        self._created = ''
        self._id_number = ''
        self._name = ''
        self._status = ''

    @property
    def id_number(self):
        '''
        The id of the task.
        '''
        return self._id_number

    @id_number.setter
    def id_number(self, value):
        self._id_number = value

    @property
    def created(self):
        '''
        The time the task was created.
        '''
        return self._created

    @created.setter
    def created(self, value):
        self._created = value

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
