import unittest
from unittest import mock

import commands.donecommand as donecommand


class DoneCommandTests(unittest.TestCase):
    def test_constructor_sets_properties(self):
        storage = mock.Mock()
        command = donecommand.DoneCommand(storage)
        self.assertEqual(storage, command.storage)
        self.assertEqual(-1, command.task_index)

    def test_task_index_property_sets_value(self):
        command = donecommand.DoneCommand(mock.Mock())
        command.task_index = 5
        self.assertEqual(5, command.task_index)

    def test_execute_calls_delete_on_storage(self):
        task1 = mock.Mock()
        task1.index = 1
        task2 = mock.Mock()
        task2.index = 2
        task3 = mock.Mock()
        task3.index = 3
        storage = mock.Mock()
        storage.delete = mock.MagicMock()
        storage.read_all = mock.MagicMock(return_value=[task1, task2, task3])
        command = donecommand.DoneCommand(storage)
        command.task_index = 2
        command.execute()
        storage.read_all.assert_called_once()
        storage.delete.assert_called_once_with(task2)


class DoneCommandParserTests(unittest.TestCase):
    def test_parse_wrong_command(self):
        args = ['wrong']
        storage = mock.Mock()
        command = donecommand.DoneCommandParser().parse(storage, args)
        self.assertEqual(None, command)

    def test_parse_no_filter(self):
        args = ['done']
        storage = mock.Mock()
        self.assertIsNone(donecommand.DoneCommandParser().parse(storage, args))            

    def test_parse_filter_not_numeric(self):
        args = ['text', 'done']
        storage = mock.Mock()
        with self.assertRaises(Exception):
            donecommand.DoneCommandParser().parse(storage, args)

    def test_parse_parse_success(self):
        args = ['2', 'done']
        storage = mock.Mock()
        parser = donecommand.DoneCommandParser()
        command = parser.parse(storage, args)
        self.assertIsInstance(command, donecommand.DoneCommand)
        self.assertEqual(2, command.task_index)
