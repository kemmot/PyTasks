'''
Module for task related entity classes.
'''

import enum

import datetime
import exceptions


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


class TaskAttributeType(enum.Enum):
    DESCRIPTION = 10
    END = 20
    ENTRY = 30
    ID = 40
    START = 50
    STATUS = 60
    WAIT = 70


class TaskAttributeName:
    DESCRIPTION = 'description'
    END = 'end'
    ENTRY = 'entry'
    ID = 'id'
    START = 'start'
    STATUS = 'status'
    UUID = 'uuid'
    WAIT = 'wait'

    @staticmethod
    def get_names():
        names = []
        names.append(TaskAttributeName.DESCRIPTION)
        names.append(TaskAttributeName.END)
        names.append(TaskAttributeName.ENTRY)
        names.append(TaskAttributeName.ID)
        names.append(TaskAttributeName.START)
        names.append(TaskAttributeName.STATUS)
        names.append(TaskAttributeName.WAIT)
        return names

    @staticmethod
    def get_name(task_type_attribute_enum):
        if task_type_attribute_enum == TaskAttributeType.DESCRIPTION:
            return TaskAttributeName.DESCRIPTION

        if task_type_attribute_enum == TaskAttributeType.END:
            return TaskAttributeName.END

        if task_type_attribute_enum == TaskAttributeType.ENTRY:
            return TaskAttributeName.ENTRY

        if task_type_attribute_enum == TaskAttributeType.ID:
            return TaskAttributeName.ID

        if task_type_attribute_enum == TaskAttributeType.START:
            return TaskAttributeName.START

        if task_type_attribute_enum == TaskAttributeType.STATUS:
            return TaskAttributeName.STATUS

        if task_type_attribute_enum == TaskAttributeType.WAIT:
            return TaskAttributeName.WAIT

        raise exceptions.NotSupportedException('Task type attribute not supported: [{}]'.format(task_type_attribute_enum))

    @staticmethod
    def is_name_valid(attribute_name):
        if attribute_name == TaskAttributeName.DESCRIPTION:
            return True

        if attribute_name == TaskAttributeName.END:
            return True

        if attribute_name == TaskAttributeName.ENTRY:
            return True

        if attribute_name == TaskAttributeName.ID:
            return True

        if attribute_name == TaskAttributeName.START:
            return True

        if attribute_name == TaskAttributeName.STATUS:
            return True

        if attribute_name == TaskAttributeName.WAIT:
            return True

        return False


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
        self._wait_time = None

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
    def is_waiting(self):
        return self.wait_time is not None and self.wait_time > datetime.datetime.now()

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

    @property
    def wait_time(self):
        '''
        The time the task is waiting until.
        '''
        return self._wait_time

    @wait_time.setter
    def wait_time(self, value):
        self._wait_time = value

    def end(self):
        self.end_time = datetime.datetime.now()

    def start(self):
        self.started_time = datetime.datetime.now()

    def stop(self):
        self.started_time = None

    def __str__(self):
        return 'index: {}, name: {}'.format(self.index, self.name)
