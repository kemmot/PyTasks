import unittest
from unittest import mock
from unittest.mock import MagicMock
import uuid

import commands
import formatters
import entities


class CommandFactoryTests(unittest.TestCase):
    def test_unknown_command(self):
        args = mock.Mock()
        args.command = 'unknown'
        factory = commands.CommandFactory('filename')
        with self.assertRaises(Exception):
            factory.get_command(args)


    def test_get_add_command(self):
        args = mock.Mock()
        args.command = 'add'
        args.name = ['first', 'task']

        filename = 'filename'
        factory = commands.CommandFactory(filename)
        command = factory.get_command(args)

        self.assertIsInstance(command, commands.AddTaskCommand)
        self.assertEqual(command.filename, filename)
        self.assertIsInstance(command.task.id_number, uuid.UUID)
        self.assertEqual(command.task.status, 'pending')
        self.assertEqual(command.task.name, ' '.join(args.name))


class AddTaskCommandTests(unittest.TestCase):
    def test_execute_writes_to_file(self):
        expected_output = 'testing 1 2 3'

        formatter = formatters.TaskWarriorFormatter()
        formatter.format = MagicMock(return_value=expected_output)

        task = entities.Task()
        task.name = 'test name'

        test_path = 'test path'
        mock_open = mock.mock_open()
        location = 'commands.open'
        with mock.patch(location, mock_open):
            command = commands.AddTaskCommand(formatter)
            command.filename = test_path
            command.task = task
            command.execute()
        mock_open.assert_called_once_with(test_path, 'a+')
        handle = mock_open()
        handle.write.assert_called_once_with(expected_output + '\n')
        handle.__exit__.assert_called()
