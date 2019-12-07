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

    def test_register_known_parsers_registers(self):
        args = mock.Mock()
        args.command = 'list'
        storage = mock.Mock()
        factory = commands.CommandFactory(storage)
        factory.register_known_parsers()
        command = factory.get_command(args)
        self.assertIsInstance(command, commands.ListTaskCommand)

class CommandBaseTests(unittest.TestCase):
    def test_execute_errors(self):
        storage = mock.MagicMock()
        command = commands.CommandBase(storage)
        with self.assertRaises(Exception):
            command.execute()


class CommandParserBaseTests(unittest.TestCase):
    def test_get_name_errors(self):
        parser = commands.CommandParserBase()
        with self.assertRaises(Exception):
            parser.get_name()

    def test_parse_errors(self):
        parser = commands.CommandParserBase()
        with self.assertRaises(Exception):
            parser.parse(mock.Mock(), mock.Mock())


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
    
    def test_execute_prints_task_id(self):
        existing_task_count = 3
        existing_tasks = []
        for count in range(0, existing_task_count):
            existing_tasks.append(mock.Mock())

        storage = mock.MagicMock()
        storage.read_all = MagicMock(return_value=existing_tasks)

        task = entities.Task()
        task.name = 'test name'

        command = commands.AddTaskCommand(storage)
        command.task = task
        
        mock_print = mock.MagicMock()
        with mock.patch('commands.print', mock_print):
            command.execute()
        output = 'Task created: {}'.format(existing_task_count + 1)
        mock_print.assert_called_once_with(output)


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


class DoneCommandTests(unittest.TestCase):
    def test_constructor_sets_properties(self):
        storage = mock.Mock()
        command = commands.DoneCommand(storage)
        self.assertEqual(storage, command.storage)
        self.assertEqual(-1, command.task_index)

    def test_task_index_property_sets_value(self):
        command = commands.DoneCommand(mock.Mock())
        command.task_index = 5
        self.assertEqual(5, command.task_index)

    def test_execute_calls_delete_on_storage(self):
        task = mock.Mock()
        storage = mock.Mock()
        storage.delete = mock.MagicMock()
        storage.read = mock.MagicMock(return_value=task)
        command = commands.DoneCommand(storage)
        command.task_index = 3
        command.execute()
        storage.read.assert_called_once_with(3)
        storage.delete.assert_called_once_with(task)


class DoneCommandParserTests(unittest.TestCase):
    def test_get_name_returns_correct_value(self):
        parser = commands.DoneCommandParser()
        self.assertEqual('done', parser.get_name())

    def test_parse_creates_correct_command(self):
        args = mock.Mock()
        args.filter = 2
        storage = mock.Mock()
        parser = commands.DoneCommandParser()
        command = parser.parse(storage, args)
        self.assertIsInstance(command, commands.DoneCommand)
        self.assertEqual(2, command.task_index)


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
