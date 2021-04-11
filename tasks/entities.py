'''
Module for task related entity classes.
'''

import datetime


class TaskAnnotation:
    def __init__(self, message, created):
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
        self._created_time = datetime.datetime.now()
        self._end_time = None
        self._id_number = ''
        self._index = -1
        self._name = ''
        self._started_time = None
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
    def created_time(self):
        '''
        The time the task was created.
        '''
        return self._created_time

    @created_time.setter
    def created_time(self, value):
        self._created_time = value

    @property
    def end_time(self):
        '''
        The time the task was completed.
        '''
        return self._end_time

    @end_time.setter
    def end_time(self, value):
        self._end_time = value

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
    def is_ended(self):
        return self.end_time is not None

    @property
    def is_started(self):
        return self.started_time is not None

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

    @property
    def started_time(self):
        '''
        The time the task was started.  None if not started.
        '''
        return self._started_time

    @started_time.setter
    def started_time(self, value):
        self._started_time = value

    def end(self):
        self.end_time = datetime.datetime.now()

    def start(self):
        self.started_time = datetime.datetime.now()

    def stop(self):
        self.started_time = None

    def __str__(self):
        return 'index: {}, name: {}'.format(self.index, self.name)
