import unittest
from unittest import mock
from unittest.mock import MagicMock

import commands.listcommand as listcommand
import filters.alwaysfilter as alwaysfilter


class ListTaskCommandTests(unittest.TestCase):
    def test_constructor_sets_storage(self):
        mock_storage = mock.Mock()
        mock_filter = mock.Mock()
        command = listcommand.ListTaskCommand(mock_storage, mock_filter)
        self.assertEqual(mock_storage, command.storage)

    def test_constructor_sets_filter(self):
        mock_storage = mock.Mock()
        mock_filter = mock.Mock()
        command = listcommand.ListTaskCommand(mock_storage, mock_filter)
        self.assertEqual(mock_filter, command.filter)

    def test_execute_calls_read_all_on_storage(self):
        tasks = []
        tasks.append(mock.MagicMock())
        tasks.append(mock.MagicMock())

        mock_storage = mock.MagicMock()
        mock_storage.read_all = MagicMock(return_value=tasks)

        mock_filter = mock.Mock()
        mock_filter.is_match = mock.MagicMock(return_value=True)

        command = listcommand.ListTaskCommand(mock_storage, mock_filter)
        command.execute()

        mock_storage.read_all.assert_called_once()

    def test_execute_filters_tasks(self):
        tasks = []
        tasks.append(mock.Mock())
        tasks.append(mock.Mock())
        tasks.append(mock.Mock())

        mock_storage = mock.Mock()
        mock_storage.read_all = MagicMock(return_value=tasks)

        mock_filter = mock.Mock()
        mock_filter.is_match = mock.Mock()
        mock_filter.is_match.side_effect = [False, True, False]

        command = listcommand.ListTaskCommand(mock_storage, mock_filter)

        mock_print = mock.MagicMock()
        with mock.patch('commands.listcommand.print', mock_print):
            command.execute()

        mock_filter.is_match.assert_called()
        calls = [mock.call('ID   Status  Description'), mock.call('------------------------'), mock.call(mock.ANY)]
        self.assertEqual(calls, mock_print.mock_calls)

    def test_execute_prints_content(self):
        task = mock.MagicMock()
        task.name = 'test1'
        task.status = 'pending'
        task.id_number = 0
        task.created = ''

        tasks = []
        tasks.append(task)

        mock_storage = mock.MagicMock()
        mock_storage.read_all = MagicMock(return_value=tasks)
        
        mock_filter = mock.Mock()
        mock_filter.is_match = mock.MagicMock(return_value=True)

        command = listcommand.ListTaskCommand(mock_storage, mock_filter)

        mock_print = mock.MagicMock()
        with mock.patch('commands.listcommand.print', mock_print):
            command.execute()

        mock_print.assert_called()


class ListTaskCommandParserTests(unittest.TestCase):
    def test_parse_wrong_command(self):
        args = ['wrong']
        mock_storage = mock.Mock()
        mock_filter_factory = mock.Mock()
        command = listcommand.ListTaskCommandParser().parse(mock_storage, mock_filter_factory, args)
        self.assertEqual(None, command)

    def test_parse_success_no_filter(self):
        args = ['list']

        mock_storage = mock.Mock()
        mock_filter = mock.Mock()
        mock_filter_factory = mock.Mock()
        mock_filter_factory.parse = mock.MagicMock(return_value=mock_filter)
        command = listcommand.ListTaskCommandParser().parse(mock_storage, mock_filter_factory, args)

        self.assertIsInstance(command, listcommand.ListTaskCommand)
        self.assertEqual(command.storage, mock_storage)
        self.assertIsInstance(command.filter, alwaysfilter.AlwaysFilter)

    def test_parse_success_with_filter(self):
        args = ['filter', 'list']

        mock_storage = mock.Mock()
        mock_filter = mock.Mock()
        mock_filter_factory = mock.Mock()
        mock_filter_factory.parse = mock.MagicMock(return_value=mock_filter)
        command = listcommand.ListTaskCommandParser().parse(mock_storage, mock_filter_factory, args)

        self.assertIsInstance(command, listcommand.ListTaskCommand)
        self.assertEqual(command.storage, mock_storage)
        self.assertEqual(command.filter, mock_filter)