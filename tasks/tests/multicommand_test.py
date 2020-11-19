import unittest
import uuid
from unittest import mock

import commands.multicommand as multicommand


class MultiCommandTests(unittest.TestCase):
    def setUp(self):
        self.mock_context = mock.Mock()
        self.mock_filter = mock.Mock()
        self.zero_item_command = mock.Mock()
        self.zero_item_command.execute = mock.MagicMock()
        self.one_item_command = mock.Mock()
        self.one_item_command.execute = mock.MagicMock()
        self.multi_item_command = mock.Mock()
        self.multi_item_command.execute = mock.MagicMock()

    def test_constructor(self):
        multicommand.MultiCommand(self.mock_context, None, None, None)

    def test_execute_no_zero_item_command(self):
        self.zero_item_command = None
        self._execute_test_no_command(0)

    def test_execute_no_one_item_command(self):
        self.one_item_command = None
        self._execute_test_no_command(1)

    def test_execute_no_multi_item_command(self):
        self.multi_item_command = None
        self._execute_test_no_command(3)

    def _execute_test_no_command(self, task_count):
        tasks = self._create_tasks(task_count)
        self.mock_filter.filter_items = mock.MagicMock(return_value=tasks)
        
        command = multicommand.MultiCommand(self.mock_context, \
            self.zero_item_command, self.one_item_command, self.multi_item_command)
        command.filter = self.mock_filter
        with self.assertRaises(Exception):
            command.execute()

    def test_execute_calls_zero_item_command(self):
        self._execute_calls_relevant_command(0)

    def test_execute_calls_one_item_command(self):
        self._execute_calls_relevant_command(1)

    def test_execute_calls_one_item_command(self):
        self._execute_calls_relevant_command(4)
    
    def _execute_calls_relevant_command(self, task_count):
        tasks = self._create_tasks(task_count)
        self.mock_filter.filter_items = mock.MagicMock(return_value=tasks)
        
        command = multicommand.MultiCommand(self.mock_context, \
            self.zero_item_command, self.one_item_command, self.multi_item_command)
        command.filter = self.mock_filter
        command.execute()

        zero_item_calls = []
        one_item_calls = []
        multi_item_calls = []
        if task_count == 0:
            zero_item_calls.append(mock.call(tasks))
        elif task_count == 1:
            one_item_calls.append(mock.call(tasks))
        else:
            multi_item_calls.append(mock.call(tasks))
        self.zero_item_command.execute_tasks.assert_has_calls(zero_item_calls)
        self.one_item_command.execute_tasks.assert_has_calls(one_item_calls)
        self.multi_item_command.execute_tasks.assert_has_calls(multi_item_calls)

    def _create_tasks(self, count, annotation_count=0):
        tasks = []
        for index in range(count):
            task = mock.Mock()
            task.annotations = []
            task.id_number = uuid.uuid4()
            task.index = index + 1
            task.name = 'task {}'.format(task.index)
            tasks.append(task)

            for annotation_index in range(0, annotation_count):
                annotation = mock.Mock()
                annotation.created = datetime.datetime(2020, 1, 1, 12, 34, 56)
                annotation.message = 'this is an annotation'
                task.annotations.append(annotation)
            
        return tasks
