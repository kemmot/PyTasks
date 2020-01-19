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
        task = mock.Mock()
        storage = mock.Mock()
        storage.delete = mock.MagicMock()
        storage.read = mock.MagicMock(return_value=task)
        command = donecommand.DoneCommand(storage)
        command.task_index = 3
        command.execute()
        storage.read.assert_called_once_with(3)
        storage.delete.assert_called_once_with(task)


class DoneCommandParserTests(unittest.TestCase):
    def test_get_name_returns_correct_value(self):
        parser = donecommand.DoneCommandParser()
        self.assertEqual('done', parser.get_name())

    def test_parse_creates_correct_command(self):
        args = mock.Mock()
        args.filter = 2
        storage = mock.Mock()
        parser = donecommand.DoneCommandParser()
        command = parser.parse(storage, args)
        self.assertIsInstance(command, donecommand.DoneCommand)
        self.assertEqual(2, command.task_index)
