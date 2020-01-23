import unittest
from unittest import mock
from unittest.mock import MagicMock
import uuid

import commands.addcommand as addcommand
import entities


class AddTaskCommandTests(unittest.TestCase):
    def test_execute_calls_write_on_storage(self):
        storage = mock.MagicMock()
        storage.write = MagicMock()

        task = entities.Task()
        task.name = 'test name'

        command = addcommand.AddTaskCommand(storage)
        command.task = task
        command.execute()

        storage.write.assert_called_once_with(task)

    def test_execute_prints_task_id(self):
        existing_task_count = 3
        existing_tasks = []
        for _ in range(0, existing_task_count):
            existing_tasks.append(mock.Mock())

        storage = mock.MagicMock()
        storage.read_all = MagicMock(return_value=existing_tasks)

        task = entities.Task()
        task.name = 'test name'

        command = addcommand.AddTaskCommand(storage)
        command.task = task

        mock_print = mock.MagicMock()
        with mock.patch('commands.addcommand.print', mock_print):
            command.execute()
        output = 'Task created: {}'.format(existing_task_count + 1)
        mock_print.assert_called_once_with(output)


class AddTaskCommandParserTests(unittest.TestCase):
    def test_parse_wrong_command(self):
        args = ['wrong']
        mock_storage = mock.Mock()
        mock_filter_factory = mock.Mock()
        command = addcommand.AddTaskCommandParser().parse(mock_storage, mock_filter_factory, args)
        self.assertEqual(None, command)

    def test_parse_no_name(self):
        args = ['add']
        mock_storage = mock.Mock()
        mock_filter_factory = mock.Mock()
        with self.assertRaises(Exception):
            addcommand.AddTaskCommandParser().parse(mock_storage, mock_filter_factory, args)

    def test_parse_returns_correct_command(self):
        args = ['add', 'first', 'task']

        mock_storage = mock.Mock()
        mock_filter_factory = mock.Mock()
        command = addcommand.AddTaskCommandParser().parse(mock_storage, mock_filter_factory, args)

        self.assertIsInstance(command, addcommand.AddTaskCommand)
        self.assertEqual(command.storage, mock_storage)
        self.assertIsInstance(command.task.id_number, uuid.UUID)
        self.assertEqual(command.task.status, 'pending')
        self.assertEqual(command.task.name, 'first task')
