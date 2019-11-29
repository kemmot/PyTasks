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

    def test_get_list_command(self):
        args = mock.Mock()
        args.command = 'list'

        filename = 'filename'
        factory = commands.CommandFactory(filename)
        command = factory.get_command(args)

        self.assertIsInstance(command, commands.ListTaskCommand)
        self.assertEqual(command.filename, filename)


class CommandBaseTests(unittest.TestCase):
    def test_filename_sets_field(self):
        command = commands.CommandBase()
        command.filename = 'test'
        self.assertEqual(command.filename, 'test')

    def test_execute_errors(self):
        command = commands.CommandBase()
        with self.assertRaises(Exception):
            command.execute()


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


class ListTaskCommandTests(unittest.TestCase):
    def test_execute_opens_and_closes_file(self):
        test_path = 'test path'

        command = commands.ListTaskCommand()
        command.filename = test_path

        mock_open = mock.mock_open()
        location = 'commands.open'
        with mock.patch(location, mock_open):
            command.execute()
        
        mock_open.assert_called_once_with(test_path, 'r')
        mock_open().__exit__.assert_called()

    def test_execute_reads_file(self):
        command = commands.ListTaskCommand()
        command.filename = 'test path'

        mock_open = mock.mock_open()
        location = 'commands.open'
        with mock.patch(location, mock_open):
            command.execute()
        
        mock_open().readlines.assert_called_once()

    def test_execute_prints_content(self):
        command = commands.ListTaskCommand()

        mock_open = mock.mock_open(read_data='task 1\ntask 2\n')
        mock_print = mock.MagicMock()
        with mock.patch('commands.open', mock_open):
            with mock.patch('commands.print', mock_print):
                command.execute()
        
        calls = [mock.call('task 1'), mock.call('task 2')]
        mock_print.assert_has_calls(calls)
