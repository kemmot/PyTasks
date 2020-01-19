import unittest
from unittest import mock
from unittest.mock import MagicMock
import uuid

import commandfactory
import entities


class CommandFactoryTests(unittest.TestCase):
    def test_get_unknown_command(self):
        args = mock.Mock()
        args.command = 'unknown'
        factory = commandfactory.CommandFactory('filename')
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
        factory = commandfactory.CommandFactory(storage)
        factory.register_parser(parser)

        command = factory.get_command(args)

        self.assertEqual(command, expected_command)
        parser.get_name.assert_called_once()
        parser.parse.assert_called_once_with(storage, args)

    def test_register_known_parsers_registers(self):
        args = mock.Mock()
        args.command = 'list'
        storage = mock.Mock()
        factory = commandfactory.CommandFactory(storage)
        factory.register_known_parsers()
        command = factory.get_command(args)
        self.assertIsInstance(command, commandfactory.ListTaskCommand)


class DoneCommandTests(unittest.TestCase):
    def test_constructor_sets_properties(self):
        storage = mock.Mock()
        command = commandfactory.DoneCommand(storage)
        self.assertEqual(storage, command.storage)
        self.assertEqual(-1, command.task_index)

    def test_task_index_property_sets_value(self):
        command = commandfactory.DoneCommand(mock.Mock())
        command.task_index = 5
        self.assertEqual(5, command.task_index)

    def test_execute_calls_delete_on_storage(self):
        task = mock.Mock()
        storage = mock.Mock()
        storage.delete = mock.MagicMock()
        storage.read = mock.MagicMock(return_value=task)
        command = commandfactory.DoneCommand(storage)
        command.task_index = 3
        command.execute()
        storage.read.assert_called_once_with(3)
        storage.delete.assert_called_once_with(task)


class DoneCommandParserTests(unittest.TestCase):
    def test_get_name_returns_correct_value(self):
        parser = commandfactory.DoneCommandParser()
        self.assertEqual('done', parser.get_name())

    def test_parse_creates_correct_command(self):
        args = mock.Mock()
        args.filter = 2
        storage = mock.Mock()
        parser = commandfactory.DoneCommandParser()
        command = parser.parse(storage, args)
        self.assertIsInstance(command, commandfactory.DoneCommand)
        self.assertEqual(2, command.task_index)


class ListTaskCommandTests(unittest.TestCase):
    def test_execute_calls_read_all_on_storage(self):
        tasks = []
        tasks.append(mock.MagicMock())
        tasks.append(mock.MagicMock())

        storage = mock.MagicMock()
        storage.read_all = MagicMock(return_value=tasks)

        command = commandfactory.ListTaskCommand(storage)
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

        command = commandfactory.ListTaskCommand(storage)

        mock_print = mock.MagicMock()
        with mock.patch('commandfactory.print', mock_print):
            command.execute()

        mock_print.assert_called()


class ListTaskCommandParserTests(unittest.TestCase):
    def test_get_list_command(self):
        args = mock.Mock()
        args.command = 'list'

        storage = mock.Mock()
        command = commandfactory.ListTaskCommandParser().parse(storage, args)

        self.assertIsInstance(command, commandfactory.ListTaskCommand)
        self.assertEqual(command.storage, storage)
