'''
Module for task related entity classes.
'''

import datetime


class TaskAnnotation:
    def __init__(self, message, created=datetime.datetime.now()):
        self._message = message
        self._created = created
    
    @property
    def created(self):
        return self._created

    @property
    def message(self):
        return self._message
    

class Task:
    '''
    A class for encapsulating task details.
    '''
    def __init__(self):
        self._annotations = []
        self._attributes = {}
        self._created = datetime.datetime.now()
        self._id_number = ''
        self._index = -1
        self._name = ''
        self._status = ''
    
    @property
    def annotations(self):
        '''
        The annotations attached to this task.
        '''
        return self._annotations
    
    @property
    def attributes(self):
        '''
        The extra attributes associated with this task.
        '''
        return self._attributes

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
    def index(self):
        '''
        The task index.
        '''
        return self._index

    @index.setter
    def index(self, value):
        self._index = value

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
