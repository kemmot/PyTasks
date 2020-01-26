'''
A module containing task formatter classes.
'''

import calendar
import datetime
import logging
import re
import os

import __main__
import entities


class TaskWarriorFormatter:
    '''
    A formatter matching task warriors file format.
    '''
    def format(self, task):
        '''
        Formats the task.
        '''
        output = '['
        output += 'description:"{}"'.format(task.name)
        output += ' entry:"{}"'.format(calendar.timegm(task.created.utctimetuple()))
        output += ' status:"{}"'.format(task.status)
        output += ' uuid:"{}"'.format(task.id_number)
        output += ']'
        return output

    def parse(self, line_number, line):
        '''
        Parses a task.
        '''
        task = entities.Task()
        task.index = line_number
        pattern = '(?P<name>\\w[^:]+):"(?P<value>[^"]+)"'
        for match in re.finditer(pattern, line):
            key = match.group('name')
            value = match.group('value')
            if key == 'description':
                task.name = value
            elif key == 'entry':
                task.created = datetime.datetime.utcfromtimestamp(float(value)/1000.)
            elif key == 'status':
                task.status = value
            elif key == 'uuid':
                task.id_number = value
        return task


class TextFileStorage:
    def __init__(self, path, formatter):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._path = path
        self._formatter = formatter       

    @property
    def formatter(self):
        return self._formatter

    @property
    def path(self):
        return self._path
    
    def delete(self, task):
        tasks_to_keep = [t for t in self.read_all() if t.id_number != task.id_number]
        self._write_all(tasks_to_keep)

    def read_all(self):
        tasks = []
        if os.path.isfile(self._path):
            with open(self._path, 'r') as file:
                line_number = 1
                for line in file.readlines():
                    line = line.strip()
                    task = self._formatter.parse(line_number, line)
                    tasks.append(task)
                    line_number += 1
        else:
            self._logger.warning('File not found: [{}]'.format(self._path))
        return tasks

    def write(self, task):
        tasks = self.read_all()
        tasks.append(task)
        self._write_all(tasks)

    def _write_all(self, tasks):
        temp_path = self._path + '.tmp'
        if os.path.isfile(temp_path):
            os.remove(temp_path)
        with open(temp_path, 'w+') as file:
            for task in tasks:
                formatted_task = self._formatter.format(task)
                file.write(formatted_task + '\n')
        file_exists = os.path.isfile(self._path)
        if file_exists:
            if os.name != 'posix':
                os.remove(self._path)
        else:
            self._logger.info('Creating new file: [{}]'.format(self._path))
        os.rename(temp_path, self._path)


class TaskWarriorStorage:
    def __init__(self, pending_storage, done_storage):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._pending_storage = pending_storage
        self._done_storage = done_storage
    
    @property
    def done_storage(self):
        return self._done_storage

    @property
    def pending_storage(self):
        return self._pending_storage

    def delete(self, task):
        self._pending_storage.delete(task)

    def read_all(self):
        return self._pending_storage.read_all()

    def write(self, task):
        self._pending_storage.write(task)


class TaskWarriorStorageCreator:
    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)
    
    def create(self, settings):
        data_location = settings.data_location

        if not os.path.isabs(data_location):
            data_location = os.path.abspath(os.path.join(os.path.dirname(__main__.__file__), data_location))
            self._logger.debug('Converted relative data location [{}] to: [{}]'.format(settings.data_location, data_location))
        
        pending_filename = settings.data_pending_filename
        pending_path = os.path.join(data_location, pending_filename)
        pending_storage = TextFileStorage(pending_path, TaskWarriorFormatter())

        done_filename = settings.data_done_filename
        done_path = os.path.join(data_location, done_filename)
        done_storage = TextFileStorage(done_path, TaskWarriorFormatter())

        return TaskWarriorStorage(pending_storage, done_storage)
