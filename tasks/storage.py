'''
A module containing task formatter classes.
'''

import calendar
import re

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
                task.created = value
            elif key == 'status':
                task.status = value
            elif key == 'uuid':
                task.id_number = value
        return task


class TaskWarriorPendingStorage:
    def __init__(self, path, formatter=TaskWarriorPendingFormatter()):
        self._path = path
        self._formatter = formatter

    def read_all(self):
        tasks = []
        with open(self._path, 'r') as file:
            line_number = 1
            for line in file.readlines():
                line = line.strip()
                task = self._formatter.parse(line_number, line)
                tasks.append(task)
                line_number += 1
        return tasks

    def write(self, task):
        with open(self._path, 'a+') as file:
            formatted_task = self._formatter.format(task)
            file.write(formatted_task + '\n')
