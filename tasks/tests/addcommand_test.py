import datetime
import unittest
from unittest import mock
from unittest.mock import MagicMock
import uuid

import commands.addcommand as addcommand
import entities


class AddTaskCommandTests(unittest.TestCase):
    def test_execute_calls_write_on_storage(self):
        mock_settings = mock.Mock()
        mock_settings.command_add_next_key_id = 2
        mock_settings.command_add_format = 'FEAT-{key_id:04}: {name}'

        mock_storage = mock.MagicMock()
        mock_storage.write = MagicMock()

        mock_context = mock.Mock()
        mock_context.settings = mock_settings
        mock_context.storage = mock_storage

        task = entities.Task()
        task.name = 'test name'

        command = addcommand.AddTaskCommand(mock_context)
        command.task = task
        command.execute()

        self.assertEqual('FEAT-0002: test name', task.name)
        mock_storage.write.assert_called_once_with(task)

    def test_execute_prints_task_id(self):
        existing_task_count = 3
        existing_tasks = []
        for _ in range(0, existing_task_count):
            existing_tasks.append(mock.Mock())

        mock_console = mock.Mock()
        mock_console.print = mock.MagicMock()

        mock_settings = mock.Mock()
        mock_settings.command_add_next_key_id = 2
        mock_settings.command_add_format = '{name}'

        mock_storage = mock.MagicMock()
        mock_storage.read_all = MagicMock(return_value=existing_tasks)

        mock_context = mock.Mock()
        mock_context.console = mock_console
        mock_context.settings = mock_settings
        mock_context.storage = mock_storage

        task = entities.Task()
        task.name = 'test name'

        command = addcommand.AddTaskCommand(mock_context)
        command.task = task
        command.execute()

        output = 'Task created: {}'.format(existing_task_count + 1)
        mock_console.print.assert_called_once_with(output)


class AddTaskCommandParserTests(unittest.TestCase):
    def test_parse_no_name(self):
        args = []
        mock_context = mock.Mock()
        with self.assertRaises(Exception):
            addcommand.AddTaskCommandParser().parse(mock_context, args)

    def test_parse_returns_correct_command(self):
        args = ['first', 'task']

        mock_context = mock.Mock()
        command = addcommand.AddTaskCommandParser().parse(mock_context, args)

        self.assertIsInstance(command, addcommand.AddTaskCommand)
        self.assertEqual(command.context, mock_context)
        self.assertIsInstance(command.task.id_number, uuid.UUID)
        self.assertEqual(command.task.status, 'pending')
        self.assertEqual(command.task.name, 'first task')

    def test_parse_parse_success_with_project_and_priority(self):
        args = ['task', 'name', 'project:test', 'priority:H', 'wait:2021-04-30']
        mock_context = mock.Mock()
        command = addcommand.AddTaskCommandParser().parse(mock_context, args)
        self.assertEqual(command.task.name, 'task name')
        self.assertEqual(len(command.task.attributes), 2)
        self.assertTrue('project' in command.task.attributes)
        self.assertEqual(command.task.attributes['project'], 'test')
        self.assertTrue('priority' in command.task.attributes)
        self.assertEqual(command.task.attributes['priority'], 'H')
        self.assertEqual(command.task.wait_time, datetime.datetime(2021, 4, 30))
