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
    DEPENDENCIES = 5
    DESCRIPTION = 10
    END = 20
    ENTRY = 30
    ID = 40
    START = 50
    STATUS = 60
    TAGS = 62
    UUID = 65
    WAIT = 70


class TaskAttributeName:
    DEPENDENCIES = 'depends'
    DESCRIPTION = 'description'
    END = 'end'
    ENTRY = 'entry'
    ID = 'id'
    START = 'start'
    STATUS = 'status'
    TAGS = 'tags'
    UUID = 'uuid'
    VTAGS = 'vtags'
    WAIT = 'wait'

    @staticmethod
    def get_names():
        names = []
        names.append(TaskAttributeName.DEPENDENCIES)
        names.append(TaskAttributeName.DESCRIPTION)
        names.append(TaskAttributeName.END)
        names.append(TaskAttributeName.ENTRY)
        names.append(TaskAttributeName.ID)
        names.append(TaskAttributeName.START)
        names.append(TaskAttributeName.STATUS)
        names.append(TaskAttributeName.TAGS)
        names.append(TaskAttributeName.UUID)
        names.append(TaskAttributeName.VTAGS)
        names.append(TaskAttributeName.WAIT)
        return names

    @staticmethod
    def get_name(task_type_attribute_enum):
        if task_type_attribute_enum == TaskAttributeType.DEPENDENCIES:
            return TaskAttributeName.DEPENDENCIES

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

        if task_type_attribute_enum == TaskAttributeType.TAGS:
            return TaskAttributeName.TAGS

        if task_type_attribute_enum == TaskAttributeType.UUID:
            return TaskAttributeName.UUID

        if task_type_attribute_enum == TaskAttributeType.VTAGS:
            return TaskAttributeName.VTAGS

        if task_type_attribute_enum == TaskAttributeType.WAIT:
            return TaskAttributeName.WAIT

        raise exceptions.NotSupportedException('Task type attribute not supported: [{}]'.format(task_type_attribute_enum))

    @staticmethod
    def is_name_valid(attribute_name):
        return attribute_name in TaskAttributeName.get_names()


class TaskAttributeRetriever:
    def get_value(self, task, attribute_name):
        if attribute_name == 'annotation.count':
            return len(task.annotations)
        elif VirtualTagName.is_name_valid(attribute_name.upper()):
            return attribute_name.upper() in task.virtual_tags
        elif TaskAttributeName.is_name_valid(attribute_name):
            return self.__get_well_known_value(task, attribute_name)
        else:
            return self.__get_attribute_value(task, attribute_name)

    def __get_well_known_value(self, task, attribute_name):
        if attribute_name == TaskAttributeName.DEPENDENCIES:
            return ','.join([str(x.index) for x in task.dependencies if not x.is_ended])
        elif attribute_name == TaskAttributeName.DESCRIPTION:
            return task.name
        elif attribute_name == TaskAttributeName.END:
            return task.end_time
        elif attribute_name == TaskAttributeName.ENTRY:
            return task.started_time
        elif attribute_name == TaskAttributeName.ID:
            return task.index
        elif attribute_name == TaskAttributeName.START:
            return task.started_time
        elif attribute_name == TaskAttributeName.STATUS:
            return task.status
        elif attribute_name == TaskAttributeName.TAGS:
            return ','.join(task.tags)
        elif attribute_name == TaskAttributeName.VTAGS:
            return ','.join(task.virtual_tags)
        elif attribute_name == TaskAttributeName.WAIT:
            return task.wait_time
        else:
            raise Exception(f'Value not supported: {attribute_name}')

    def __get_attribute_value(self, task, attribute_name):
        if attribute_name in task.attributes:
            return task.attributes[attribute_name]
        else:
            return ''


class Task:
    '''
    A class for encapsulating task details.
    '''
    def __init__(self):
        self._annotations = []
        self._attributes = {}
        self._created_time = datetime.datetime.now()
        self._dependencies = []
        self._dependency_ids = []
        self._end_time = None
        self._id_number = ''
        self._index = -1
        self._name = ''
        self._started_time = None
        self._status = ''
        self._tags = []
        self._wait_time = None

    @property
    def all_tags(self):
        return self.tags + self.virtual_tags

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
    def dependencies(self):
        return self._dependencies

    @property
    def dependency_ids(self):
        return self._dependency_ids

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
    def is_blocked(self):
        for dependency in self.dependencies:
            if not dependency.is_ended:
                return True
        return False

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
    def tags(self):
        return self._tags
    
    @property
    def virtual_tags(self):
        vtags = []
        if self.is_blocked: vtags.append(VirtualTagName.BLOCKED)
        if self.is_started: vtags.append(VirtualTagName.STARTED)
        if self.is_waiting: vtags.append(VirtualTagName.WAITING)
        return vtags

    @property
    def wait_time(self):
        '''
        The time the task is waiting until.
        '''
        return self._wait_time

    @wait_time.setter
    def wait_time(self, value):
        self._wait_time = value
    
    def add_tag(self, tag_name):
        if tag_name.upper() in VirtualTagName.get_names():
            raise Exception('Cannot add virtual tag: {}'.format(tag_name))
        if not tag_name in self._tags:
            self._tags.append(tag_name)

    def end(self):
        self.end_time = datetime.datetime.now()
    
    def remove_tag(self, tag_name):
        if tag_name.upper() in VirtualTagName.get_names():
            raise Exception('Cannot remove virtual tag: {}'.format(tag_name))
        if tag_name in self._tags:
            self._tags.remove(tag_name)

    def start(self):
        self.started_time = datetime.datetime.now()

    def stop(self):
        self.started_time = None

    def __str__(self):
        return 'index: {}, name: {}'.format(self.index, self.name)


class VirtualTagType(enum.Enum):
    BLOCKED = 10
    STARTED = 20
    WAITING = 30


class VirtualTagName:
    BLOCKED = 'BLOCKED'
    STARTED = 'STARTED'
    WAITING = 'WAITING'

    @staticmethod
    def get_names():
        names = []
        names.append(VirtualTagName.BLOCKED)
        names.append(VirtualTagName.STARTED)
        names.append(VirtualTagName.WAITING)
        return names

    @staticmethod
    def get_name(virtual_tag_type_enum):
        if virtual_tag_type_enum == TaskAttributeType.BLOCKED:
            return TaskAttributeName.BLOCKED
        elif virtual_tag_type_enum == TaskAttributeType.STARTED:
            return TaskAttributeName.STARTED
        elif virtual_tag_type_enum == TaskAttributeType.WAITING:
            return TaskAttributeName.WAITING
        raise exceptions.NotSupportedException('Virtual tag not supported: [{}]'.format(virtual_tag_type_enum))

    @staticmethod
    def is_name_valid(name):
        return name in VirtualTagName.get_names()
