'''
A module containing task formatter classes.
'''

import calendar
import copy
import datetime
import logging
import re
import os
import time
import uuid

import __main__
import entities


class EditFormatter:
    def format(self, task):
        output = ''
        output += self._format_comment_line('lines beginning with ''#'' will be ignored')
        output += self._format_comment_line(self._format_key_value_line('uuid', task.id_number, end=''))
        output += self._format_comment_line(self._format_key_value_line('created time', task.created_time, end=''))
        output += self._format_key_value_line(entities.TaskAttributeName.DESCRIPTION, task.name)
        output += self._format_key_value_line(entities.TaskAttributeName.STATUS, task.status)
        output += self._format_key_value_line(entities.TaskAttributeName.START, task.started_time)
        output += self._format_key_value_line(entities.TaskAttributeName.END, task.end_time)
        output += self._format_key_value_line(entities.TaskAttributeName.WAIT, task.wait_time)
        
        tag_string = entities.TaskAttributeRetriever().get_value(task, entities.TaskAttributeName.TAGS)
        output += self._format_key_value_line(entities.TaskAttributeName.TAGS, tag_string)

        output += self._format_empty_line()
        output += self._format_comment_line('dependencies')
        for dependency in sorted(task.dependencies):
            output += self._format_line(dependency)

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
                key_lower = key.lower()
                value = ':'.join(parts[1:]).strip()
                if key_lower == entities.TaskAttributeName.DESCRIPTION:
                    task.name = value
                elif key_lower == entities.TaskAttributeName.END:
                    task.end_time = self._parse_datetime(value)
                elif key_lower == entities.TaskAttributeName.START:
                    task.started_time = self._parse_datetime(value)
                elif key_lower == entities.TaskAttributeName.STATUS:
                    task.status = value
                elif key_lower == entities.TaskAttributeName.TAGS:
                    for tag_name in value.split(','):
                        task.add_tag(tag_name)
                elif key_lower == entities.TaskAttributeName.WAIT:
                    task.wait_time = self._parse_datetime(value)
                else:
                    task.attributes[key] = value
            else:
                id = self._try_parse_guid(line)
                if id:
                    task.dependency_ids.append(id)
        return task

    def _parse_datetime(self, string_value):
        if not string_value:
            return None
        return datetime.datetime.strptime(string_value, '%Y-%m-%d %H:%M:%S')
    
    def _try_parse_guid(self, string_value):
        try:
            return uuid.UUID(string_value)
        except ValueError:
            return None 


class TaskWarriorFormatter:
    '''
    A formatter matching task warriors file format.
    '''
    def format(self, task):
        '''
        Formats the task.
        '''
        output_key_values = {}
        output_key_values[entities.TaskAttributeName.DESCRIPTION] = task.name
        output_key_values[entities.TaskAttributeName.ENTRY] = calendar.timegm(task.created_time.utctimetuple())
        output_key_values[entities.TaskAttributeName.STATUS] = task.status
        output_key_values[entities.TaskAttributeName.UUID] = task.id_number

        if task.is_started:
            output_key_values[entities.TaskAttributeName.START] = calendar.timegm(task.started_time.utctimetuple())

        if task.is_ended:
            output_key_values[entities.TaskAttributeName.END] = calendar.timegm(task.end_time.utctimetuple())

        if task.wait_time:
            output_key_values[entities.TaskAttributeName.WAIT] = calendar.timegm(task.wait_time.utctimetuple())

        for annotation in task.annotations:
            created_output = calendar.timegm(annotation.created.utctimetuple())
            output_key_values['annotation_{}'.format(created_output)] = annotation.message

        tag_string = entities.TaskAttributeRetriever().get_value(task, entities.TaskAttributeName.TAGS)
        if tag_string:
            output_key_values[entities.TaskAttributeName.TAGS] = tag_string

        for attribute_name, attribute_value in task.attributes.items():
            output_key_values[attribute_name] = attribute_value

        dependency_index = 0
        for dependency_id in task.dependency_ids:
            output_key_values['dependency_{}'.format(dependency_index)] = dependency_id
            dependency_index += 1

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
            if key == entities.TaskAttributeName.DESCRIPTION:
                task.name = value
            elif key == entities.TaskAttributeName.END:
                task.end_time = self._parse_datetime(value)
            elif key == entities.TaskAttributeName.ENTRY:
                task.created_time = self._parse_datetime(value)
            elif key == entities.TaskAttributeName.START:
                task.started_time = self._parse_datetime(value)
            elif key == entities.TaskAttributeName.STATUS:
                task.status = value
            elif key == entities.TaskAttributeName.TAGS:
                for tag_name in value.split(','):
                    task.add_tag(tag_name)
            elif key == entities.TaskAttributeName.UUID:
                task.id_number = uuid.UUID(value)
            elif key == entities.TaskAttributeName.WAIT:
                task.wait_time = self._parse_datetime(value)
            elif key.startswith('annotation_'):
                created_timestamp = key[11:]
                annotation_created = self._parse_datetime(created_timestamp)
                annotation = entities.TaskAnnotation(value, annotation_created)
                task.annotations.append(annotation)
            elif key.startswith('dependency_'):
                task.dependency_ids.append(uuid.UUID(value))
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
    def __init__(self, path, formatter, undo_log=None):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._path = path
        self._formatter = formatter
        self._undo_log = undo_log

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
            if self._undo_log:
                self._undo_log.log_addition(task)
        self._replace_all(existing_tasks)

    def update(self, tasks):
        original_tasks = self.read_all()
        tasks_to_keep = []
        for original_task in original_tasks:
            task_to_keep = original_task
            for task_to_update in tasks:
                if original_task.id_number == task_to_update.id_number:
                    task_to_keep = task_to_update
                    if self._undo_log:
                        self._undo_log.log_update(original_task)
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
    def __init__(self, pending_storage, done_storage, undo_log):
        self._logger = logging.getLogger(self.__class__.__name__)
        self._pending_storage = pending_storage
        self._done_storage = done_storage
        self._undo_log = undo_log

    @property
    def done_storage(self):
        return self._done_storage

    @property
    def pending_storage(self):
        return self._pending_storage

    @property
    def undo_log(self):
        return self._undo_log

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
        pending_tasks = self._pending_storage.read_pending()
        complete_tasks = self.done_storage.read_all()
        all_tasks = pending_tasks + complete_tasks
        self.__populate_dependencies(pending_tasks, all_tasks)
        return pending_tasks

    def __populate_dependencies(self, pending_tasks, all_tasks):
        tasks_by_id = {}
        for task in all_tasks:
            tasks_by_id[task.id_number] = task
        for task in pending_tasks:
            for dependency_id in task.dependency_ids:
                if dependency_id in tasks_by_id:
                    task.dependencies.append(tasks_by_id[dependency_id])

    def update(self, tasks):
        self._pending_storage.update(tasks)

    def write(self, task):
        tasks = []
        tasks.append(task)
        self._pending_storage.write(tasks)


class UndoLog:
    def __init__(self, storage):
        self._storage = storage
    
    def recent_sort(t):
        return t.attributes['__change_date__']
    
    def get_most_recent_change(self):
        changes = self._storage.read_all()
        if not changes:
            return None
        changes.sort(key = UndoLog.recent_sort)
        changes.reverse()
        return changes[0]

    def log_addition(self, task):
        self._log_change('NEW', task)

    def log_update(self, task):
        self._log_change('UPDATE', task)

    def _log_change(self, change_type, task):
        clone = copy.deepcopy(task)
        clone.attributes['__change_date__'] = datetime.datetime.now()
        clone.attributes['__change_type__'] = change_type
        tasks = []
        tasks.append(clone)
        self._storage.write(tasks)


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
        
        undo_filename = settings.data_undo_filename
        undo_path = os.path.join(data_location, undo_filename)
        undo_storage = TextFileStorage(undo_path, TaskWarriorFormatter())
        undo_log = UndoLog(undo_storage)

        pending_filename = settings.data_pending_filename
        pending_path = os.path.join(data_location, pending_filename)
        pending_storage = TextFileStorage(pending_path, TaskWarriorFormatter(), undo_log)

        done_filename = settings.data_done_filename
        done_path = os.path.join(data_location, done_filename)
        done_storage = TextFileStorage(done_path, TaskWarriorFormatter())

        return TaskWarriorStorage(pending_storage, done_storage, undo_log)
