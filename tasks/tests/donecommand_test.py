import unittest
from unittest import mock

import commands.donecommand as donecommand


class DoneCommandTests(unittest.TestCase):
    def test_constructor_sets_properties(self):
        storage = mock.Mock()
        filter = mock.Mock()
        command = donecommand.DoneCommand(storage, filter)
        self.assertEqual(storage, command.storage)
        self.assertEqual(filter, command.filter)

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
        filter = mock.MagicMock()
        filter.is_match = mock.Mock()
        filter.is_match.side_effect = [False, True, False]
        command = donecommand.DoneCommand(storage, filter)
        command.task_index = 2
        command.execute()
        storage.read_all.assert_called_once()
        storage.delete.assert_called_once_with(task2)


class DoneCommandParserTests(unittest.TestCase):
    def test_parse_wrong_command(self):
        args = ['wrong']
        mock_storage = mock.Mock()
        mock_filter_factory = mock.Mock()
        command = donecommand.DoneCommandParser().parse(mock_storage, mock_filter_factory, args)
        self.assertEqual(None, command)

    def test_parse_no_filter(self):
        args = ['done']
        mock_storage = mock.Mock()
        mock_filter_factory = mock.Mock()
        self.assertIsNone(donecommand.DoneCommandParser().parse(mock_storage, mock_filter_factory, args))

    def test_parse_no_filter_parsed(self):
        args = ['text', 'done']
        mock_storage = mock.Mock()
        mock_filter_factory = mock.Mock()
        mock_filter_factory.parse = mock.MagicMock()
        mock_filter_factory.parse.side_effect = Exception
        with self.assertRaises(Exception):
            donecommand.DoneCommandParser().parse(mock_storage, mock_filter_factory, args)

    def test_parse_parse_success(self):
        args = ['2', 'done']
        mock_storage = mock.Mock()
        mock_filter_factory = mock.Mock()
        mock_filter = mock.Mock()
        mock_filter_factory.parse = mock.MagicMock(return_value=mock_filter)
        parser = donecommand.DoneCommandParser()
        command = parser.parse(mock_storage, mock_filter_factory, args)
        self.assertIsInstance(command, donecommand.DoneCommand)
        self.assertEqual(mock_filter, command.filter)
