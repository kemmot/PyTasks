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


class TaskWarriorPendingFormatter:
    '''
    A formatter matching task warriors pending file format.
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


class TaskWarriorPendingStorage:
    def __init__(self, path, formatter=TaskWarriorPendingFormatter()):
        self._logger = logging.getLogger(self.__class__.__name__)
        if not os.path.isabs(path):
            path = os.path.join(os.path.dirname(os.path.abspath(__main__.__file__)), path)
            self._logger.debug('Converted relative path to: [{}]'.format(path))
        self._path = path
        self._formatter = formatter
    
    @property
    def path(self):
        return self._path

    def delete(self, task):
        tasks_to_keep = [t for t in self.read_all() if t.id_number != task.id_number]
        self._write_all(tasks_to_keep)

    def read(self, task_index):
        results = [t for t in self.read_all() if t.index == task_index]
        if not results:
            raise IndexError('Task index not found: {}'.format(task_index))
        return results[0]

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
