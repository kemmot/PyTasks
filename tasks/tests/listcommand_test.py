import unittest
from unittest import mock
from unittest.mock import MagicMock

import commands.listcommand as listcommand


class ListTaskCommandTests(unittest.TestCase):
    def test_constructor_sets_storage(self):
        mock_context = mock.Mock()
        mock_filter = mock.Mock()
        command = listcommand.ListTaskCommand(mock_context, mock_filter)
        self.assertEqual(mock_context, command.context)

    def test_constructor_sets_filter(self):
        mock_context = mock.Mock()
        mock_filter = mock.Mock()
        command = listcommand.ListTaskCommand(mock_context, mock_filter)
        self.assertEqual(mock_filter, command.filter)

    def test_before_execute_calls_garbage_collect_on_storage(self):
        mock_context = self._create_mock_context([])
        mock_filter = mock.Mock()
        command = listcommand.ListTaskCommand(mock_context, mock_filter)
        command.before_execute()
        mock_context.storage.garbage_collect.assert_called_once()

    def test_execute_calls_read_all_on_storage(self):
        tasks = []
        tasks.append(mock.MagicMock())
        tasks.append(mock.MagicMock())
        mock_context = self._create_mock_context(tasks)

        mock_filter = mock.Mock()
        mock_filter.filter_items = mock.MagicMock(return_value=tasks)

        command = listcommand.ListTaskCommand(mock_context, mock_filter)
        command.execute()

        mock_context.storage.read_all.assert_called_once()

    def test_execute_filters_tasks(self):
        tasks = []
        tasks.append(mock.Mock())
        tasks.append(mock.Mock())
        tasks.append(mock.Mock())
        tasks[1].index = 2
        tasks[1].is_ended = False
        tasks[1].status = 'this status'
        tasks[1].name = 'some name'
        tasks[1].is_ended = False

        mock_context = self._create_mock_context(tasks)

        mock_filter = mock.Mock()
        mock_filter.filter_items = mock.MagicMock(return_value=[tasks[1]])

        command = listcommand.ListTaskCommand(mock_context, mock_filter)
        command.execute()

        mock_filter.filter_items.assert_called()

        add_column_call1 = mock.call('ID')
        add_column_call2 = mock.call('Status')
        add_column_call3 = mock.call('Description')
        add_column_calls = [add_column_call1, add_column_call2, add_column_call3]
        self.assertEqual(add_column_calls, mock_context.mock_table.add_column.mock_calls)

        add_row_call1 = mock.call(2, 'this status', 'some name')
        add_row_calls = [add_row_call1]
        self.assertEqual(add_row_calls, mock_context.mock_table.add_row.mock_calls)

        mock_context.console.print_lines.assert_called()

    def test_execute_prints_content(self):
        task = mock.MagicMock()
        task.name = 'test1'
        task.status = 'pending'
        task.id_number = 0
        task.created = ''

        tasks = []
        tasks.append(task)

        command = self._create_command(tasks, tasks)
        command.execute()

        command.context.console.parse_backcolour.assert_called_with('black')
        command.context.console.parse_forecolour.assert_called_with('white')
        command.context.console.print_lines.assert_called()

    def test_execute_raises_on_invalid_backcolour(self):
        command = self._create_command()
        command.context.console.parse_backcolour.side_effect = Exception()
        with self.assertRaises(Exception):
            command.execute()

    def test_execute_raises_on_invalid_forecolour(self):
        command = self._create_command()
        command.context.console.parse_forecolour.side_effect = Exception()
        with self.assertRaises(Exception):
            command.execute()

    def _create_command(self, tasks=[], filter_tasks=[]):
        mock_context = self._create_mock_context(tasks)

        mock_filter = mock.Mock()
        mock_filter.filter_items = mock.MagicMock(return_value=filter_tasks)

        return listcommand.ListTaskCommand(mock_context, mock_filter)

    def _create_mock_context(self, tasks=[]):
        mock_table = mock.Mock()
        mock_table.add_column = mock.MagicMock()
        mock_table.add_row = mock.MagicMock()
        mock_table.create_output = MagicMock(return_value='')

        mock_console = mock.Mock()
        mock_console.parse_backcolour = mock.MagicMock(return_value='')
        mock_console.print_lines = mock.MagicMock()

        mock_storage = mock.MagicMock()
        mock_storage.read_all = MagicMock(return_value=tasks)

        mock_context = mock.Mock()
        mock_context.console = mock_console
        mock_context.create_table = mock.MagicMock(return_value=mock_table)
        mock_context.storage = mock_storage
        mock_context.mock_table = mock_table

        mock_context.settings.table_row_alt_backcolour = 'black'
        mock_context.settings.table_row_alt_forecolour = 'white'
        mock_context.settings.table_row_backcolour = 'black'
        mock_context.settings.table_row_forecolour = 'white'

        return mock_context


class ListTaskCommandParserTests(unittest.TestCase):
    def test_parse_success_no_filter(self):
        args = []

        mock_filter = mock.Mock()
        mock_filter_factory = mock.Mock()
        mock_filter_factory.parse = mock.MagicMock(return_value=mock_filter)

        mock_context = mock.Mock()
        mock_context.filter_factory = mock_filter_factory

        command = listcommand.ListTaskCommandParser().parse(mock_context, args)

        self.assertIsInstance(command, listcommand.ListTaskCommand)
        self.assertEqual(command.context, mock_context)
