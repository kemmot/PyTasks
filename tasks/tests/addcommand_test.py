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
        
        mock_settings = mock.Mock()
        mock_settings.command_add_next_key_id = 2
        mock_settings.command_add_format = '{name}'

        mock_storage = mock.MagicMock()
        mock_storage.read_all = MagicMock(return_value=existing_tasks)
        
        mock_context = mock.Mock()
        mock_context.settings = mock_settings
        mock_context.storage = mock_storage

        task = entities.Task()
        task.name = 'test name'

        command = addcommand.AddTaskCommand(mock_context)
        command.task = task

        mock_print = mock.MagicMock()
        with mock.patch('commands.addcommand.print', mock_print):
            command.execute()
        output = 'Task created: {}'.format(existing_task_count + 1)
        mock_print.assert_called_once_with(output)


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
