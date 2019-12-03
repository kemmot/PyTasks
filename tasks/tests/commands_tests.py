import unittest
from unittest import mock
from unittest.mock import MagicMock
import uuid

import commands
import entities


class CommandFactoryTests(unittest.TestCase):
    def test_get_unknown_command(self):
        args = mock.Mock()
        args.command = 'unknown'
        factory = commands.CommandFactory('filename')
        with self.assertRaises(Exception):
            factory.get_command(args)

    def test_get_known_command(self):
        args = mock.Mock()
        args.command = 'add'

        expected_command = mock.Mock()

        parser = mock.Mock()
        parser.get_name = mock.MagicMock(return_value=args.command)
        parser.parse = mock.MagicMock(return_value=expected_command)

        storage = mock.Mock()
        factory = commands.CommandFactory(storage)
        factory.register_parser(parser)
        
        command = factory.get_command(args)

        self.assertEqual(command, expected_command)
        parser.get_name.assert_called_once()
        parser.parse.assert_called_once_with(storage, args)


class CommandBaseTests(unittest.TestCase):
    def test_execute_errors(self):
        storage = mock.MagicMock()
        command = commands.CommandBase(storage)
        with self.assertRaises(Exception):
            command.execute()


class AddTaskCommandTests(unittest.TestCase):
    def test_execute_calls_write_on_storage(self):
        storage = mock.MagicMock()
        storage.write = MagicMock()

        task = entities.Task()
        task.name = 'test name'

        command = commands.AddTaskCommand(storage)
        command.task = task
        command.execute()

        storage.write.assert_called_once_with(task)


class AddTaskCommandParserTests(unittest.TestCase):
    def test_parse_returns_correct_command(self):
        args = mock.Mock()
        args.command = 'add'
        args.name = ['first', 'task']

        storage = mock.Mock()
        command = commands.AddTaskCommandParser().parse(storage, args)

        self.assertIsInstance(command, commands.AddTaskCommand)
        self.assertEqual(command.storage, storage)
        self.assertIsInstance(command.task.id_number, uuid.UUID)
        self.assertEqual(command.task.status, 'pending')
        self.assertEqual(command.task.name, ' '.join(args.name))


class ListTaskCommandTests(unittest.TestCase):
    def test_execute_calls_read_all_on_storage(self):
        tasks = []
        tasks.append(mock.MagicMock())
        tasks.append(mock.MagicMock())

        storage = mock.MagicMock()
        storage.read_all = MagicMock(return_value=tasks)

        command = commands.ListTaskCommand(storage)
        command.execute()

        storage.read_all.assert_called_once()

    def test_execute_prints_content(self):
        task = mock.MagicMock()
        task.name = 'test1'
        task.status = 'pending'
        task.id_number = 0
        task.created = ''

        tasks = []
        tasks.append(task)

        storage = mock.MagicMock()
        storage.read_all = MagicMock(return_value=tasks)

        command = commands.ListTaskCommand(storage)

        mock_print = mock.MagicMock()
        with mock.patch('commands.print', mock_print):
            command.execute()

        mock_print.assert_called()


class ListTaskCommandParserTests(unittest.TestCase):
    def test_get_list_command(self):
        args = mock.Mock()
        args.command = 'list'

        storage = mock.Mock()
        command = commands.ListTaskCommandParser().parse(storage, args)

        self.assertIsInstance(command, commands.ListTaskCommand)
        self.assertEqual(command.storage, storage)