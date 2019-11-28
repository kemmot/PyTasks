import unittest
from unittest import mock
from unittest.mock import MagicMock

import commands
import formatters
import entities


class CommandFactoryTests(unittest.TestCase):
    def test_unknown_command(self):
        args = mock.Mock()
        args.command = 'unknown'
        factory = commands.CommandFactory('filename')
        with self.assertRaises(Exception):
            command = factory.get_command(args)


    def test_get_add_command(self):
        args = mock.Mock()
        args.command = 'add'
        args.name = ['first','task']

        filename = 'filename'
        factory = commands.CommandFactory(filename)
        command = factory.get_command(args)

        self.assertIsInstance(command, commands.AddTaskCommand)
        self.assertEqual(command.filename, filename)
        self.assertEqual(command.task.name, ' '.join(args.name))


class AddTaskCommandTests(unittest.TestCase):
    def test_execute_writes_to_file(self):
        expected_output = 'testing 1 2 3'

        formatter = formatters.TaskWarriorFormatter()
        formatter.format = MagicMock(return_value=expected_output)

        task1 = entities.Task()
        task1.name = 'test name'

        test_path = 'test path'
        m = mock.mock_open()
        location = 'commands.open'
        with mock.patch(location, m) as mock_open:
            command = commands.AddTaskCommand(formatter)
            command.filename = test_path
            command.task = task1
            command.execute()
        m.assert_called_once_with(test_path, 'a+')
        handle = m()
        handle.write.assert_called_once_with(expected_output + '\n')
        handle.__exit__.assert_called()

