'''
A module containing task formatter classes.
'''

import calendar
import datetime
import logging
import re
import os
import time

import __main__
import entities


class EditFormatter:
    def format(self, task):
        output = ''
        output += self._format_comment_line('lines beginning with ''#'' will be ignored')
        output += self._format_comment_line(self._format_key_value_line('uuid', task.id_number, end=''))
        output += self._format_comment_line(self._format_key_value_line('created time', task.created_time, end=''))
        output += self._format_key_value_line('description', task.name)
        output += self._format_key_value_line('status', task.status)
        output += self._format_key_value_line('start', task.started_time)
        output += self._format_key_value_line('end', task.end_time)
        output += self._format_key_value_line('wait', task.wait_time)

        output += self._format_empty_line()
        output += self._format_comment_line('custom attributes')
        output += self._format_comment_line('key: value')
        for name in sorted(task.attributes):
            value = task.attributes[name]
            output += self._format_key_value_line(name, value)

        output += self._format_empty_line()
        output += self._format_comment_line('annotations')
        output += self._format_comment_line('yyyy-MM-dd HH:mm:ss: annotation comment')
        for annotation in task.annotations:
            output += self._format_key_value_line(annotation.created, annotation.message)

        return output
    
    def _format_comment_line(self, line):
        return self._format_line('# ' + line)
    
    def _format_empty_line(self):
        return self._format_line('')
    
    def _format_key_value_line(self, key, value, end='\n'):
        value_to_print = value if value else ''
        return self._format_line(f'{key}: {value_to_print}', end)

    def _format_line(self, line, end='\n'):
        return line + end

    def parse(self, lines):
        task = entities.Task()
        for line in lines:
            line = line.strip()
            annotation_match = re.search('(?P<created>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}): (?P<message>.+)', line)
            if line == '' or line.startswith('#'):
                # comment or non-editable field
                continue
            elif annotation_match != None:
                created = datetime.datetime.strptime(annotation_match.group('created'), '%Y-%m-%d %H:%M:%S')
                message = annotation_match.group('message')
                annotation = entities.TaskAnnotation(message, created)
                task.annotations.append(annotation)
            elif ':' in line:
                parts = line.split(':')
                key = parts[0]
                key_upper = key.upper()
                value = ':'.join(parts[1:]).strip()
                if key_upper == 'DESCRIPTION':
                    task.name = value
                elif key_upper == 'END':
                    task.end_time = self._parse_datetime(value)
                elif key_upper == 'START':
                    task.started_time = self._parse_datetime(value)
                elif key_upper == 'STATUS':
                    task.status = value
                elif key_upper == 'WAIT':
                    task.wait_time = self._parse_datetime(value)
                else:
                    task.attributes[key] = value
        return task

    def _parse_datetime(self, string_value):
        if not string_value:
            return None
        return datetime.datetime.strptime(string_value, '%Y-%m-%d %H:%M:%S')



class TaskWarriorFormatter:
    '''
    A formatter matching task warriors file format.
    '''
    def format(self, task):
        '''
        Formats the task.
        '''

        output_key_values = {}
        output_key_values['description'] = task.name
        output_key_values['entry'] = calendar.timegm(task.created_time.utctimetuple())
        output_key_values['status'] = task.status
        output_key_values['uuid'] = task.id_number

        if task.is_started:
            output_key_values['start'] = calendar.timegm(task.started_time.utctimetuple())

        if task.is_ended:
            output_key_values['end'] = calendar.timegm(task.end_time.utctimetuple())

        if task.wait_time:
            output_key_values['wait'] = calendar.timegm(task.wait_time.utctimetuple())

        for annotation in task.annotations:
            created_output = calendar.timegm(annotation.created.utctimetuple())
            output_key_values['annotation_{}'.format(created_output)] = annotation.message

        for attribute_name, attribute_value in task.attributes.items():
            output_key_values[attribute_name] = attribute_value

        output = '['
        first_value = True
        for key, value in sorted(output_key_values.items()):
            if first_value:
                first_value = False
            else:
                output += ' '
            output += '{}:"{}"'.format(key, value)
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
            elif key == 'end':
                task.end_time = self._parse_datetime(value)
            elif key == 'entry':
                task.created_time = self._parse_datetime(value)
            elif key == 'start':
                task.started_time = self._parse_datetime(value)
            elif key == 'status':
                task.status = value
            elif key == 'uuid':
                task.id_number = value
            elif key == 'wait':
                task.wait_time = self._parse_datetime(value)
            elif key.startswith('annotation_'):
                created_timestamp = key[11:]
                annotation_created = self._parse_datetime(created_timestamp)
                annotation = entities.TaskAnnotation(value, annotation_created)
                task.annotations.append(annotation)
            else:
                task.attributes[key] = value
        return task

    def _parse_datetime(self, seconds_since_epoc_string):
        created_utc_time_struct = time.gmtime(float(seconds_since_epoc_string))
        return datetime.datetime( \
            created_utc_time_struct.tm_year,
            created_utc_time_struct.tm_mon,
            created_utc_time_struct.tm_mday,
            created_utc_time_struct.tm_hour,
            created_utc_time_struct.tm_min,
            created_utc_time_struct.tm_sec)


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

    def delete(self, tasks):
        tasks_to_keep = []
        for existing_task in self.read_all():
            keep = True
            for task in tasks:
                if task.id_number == existing_task.id_number:
                    keep = False
                    break
            if keep:
                tasks_to_keep.append(existing_task)
        self._replace_all(tasks_to_keep)

    def read_pending(self):
        return [t for t in self.read_all() if not t.is_ended]

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
            self._logger.warning('File not found: [%s]', self._path)
        return tasks

    def write(self, tasks):
        existing_tasks = self.read_all()
        for task in tasks:
            existing_tasks.append(task)
        self._replace_all(existing_tasks)

    def update(self, tasks):
        original_tasks = self.read_all()
        tasks_to_keep = []
        for original_task in original_tasks:
            task_to_keep = original_task
            for task_to_update in tasks:
                if original_task.id_number == task_to_update.id_number:
                    task_to_keep = task_to_update
                    break
            tasks_to_keep.append(task_to_keep)
        self._replace_all(tasks_to_keep)

    def _replace_all(self, tasks):
        temp_path = self._path + '.tmp'
        if os.path.isfile(temp_path):
            os.remove(temp_path)
        with open(temp_path, 'w+', newline='\n') as file:
            for task in tasks:
                formatted_task = self._formatter.format(task)
                file.write(formatted_task + '\n')
        file_exists = os.path.isfile(self._path)
        if file_exists:
            if os.name != 'posix':
                os.remove(self._path)
        else:
            self._logger.info('Creating new file: [%s]', self._path)
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

    def garbage_collect(self):
        done_tasks = []
        for task in self._pending_storage.read_all():
            if task.is_ended:
                done_tasks.append(task)
        self._done_storage.write(done_tasks)
        self._pending_storage.delete(done_tasks)
        if done_tasks:
            message = 'Garbage collected %s complete tasks to done file'
            self._logger.info(message, len(done_tasks))
        else:
            self._logger.debug('No garbage collection required')

    def read_all(self):
        return self._pending_storage.read_pending()

    def update(self, tasks):
        self._pending_storage.update(tasks)

    def write(self, task):
        tasks = []
        tasks.append(task)
        self._pending_storage.write(tasks)


class TaskWarriorStorageCreator:
    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)

    def create(self, settings):
        data_location = settings.data_location

        if not os.path.isabs(data_location):
            data_location = os.path.expanduser(data_location)
            if not os.path.isabs(data_location):
                data_location = os.path.join(os.path.dirname(__main__.__file__), data_location)
            data_location = os.path.abspath(data_location)
            message = 'Converted relative data location [%s] to: [%s]'
            self._logger.debug(message, settings.data_location, data_location)

        pending_filename = settings.data_pending_filename
        pending_path = os.path.join(data_location, pending_filename)
        pending_storage = TextFileStorage(pending_path, TaskWarriorFormatter())

        done_filename = settings.data_done_filename
        done_path = os.path.join(data_location, done_filename)
        done_storage = TextFileStorage(done_path, TaskWarriorFormatter())

        return TaskWarriorStorage(pending_storage, done_storage)
