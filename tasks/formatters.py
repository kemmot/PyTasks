'''
A module containing task formatter classes.
'''

import re

import entities


class TaskWarriorFormatter:
    '''
    A formatter matching task warriors internal file format.
    '''
    def format(self, task):
        '''
        Formats the task.
        '''
        output = '['
        output += 'description:"{}"'.format(task.name)
        output += ' entry:"{}"'.format(task.created.strftime('%s'))
        output += ' status:"{}"'.format(task.status)
        output += ' uuid:"{}"'.format(task.id_number)
        output += ']'
        return output

    def parse(self, line):
        '''
        Parses a task.
        '''
        task = entities.Task()
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
