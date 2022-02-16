import unittest
from unittest import mock

import commands.columnscommand as columnscommand


class ColumnsCommandTests(unittest.TestCase):
    def test_constructor_sets_properties(self):
        mock_context = mock.Mock()
        mock_filter = mock.Mock()
        command = columnscommand.ColumnsCommand(mock_context, mock_filter)
        self.assertEqual(mock_context, command.context)
        self.assertEqual(mock_filter, command.filter)

    def test_execute_calls_read_all_on_storage(self):
        tasks = self._create_tasks(3)
        mock_context = self._create_context(tasks)

        mock_filter = mock.MagicMock()
        mock_filter.is_match = mock.MagicMock(return_value=True)

        command = columnscommand.ColumnsCommand(mock_context, mock_filter)
        command.execute()

        mock_context.storage.read_all.assert_called_once()

    def test_execute_prints_well_known_columns(self):
        tasks = self._create_tasks(3)
        tasks[0].attributes['project'] = 'project1'
        tasks[1].attributes['project'] = 'project2'
        mock_context = self._create_context(tasks)

        mock_filter = mock.MagicMock()
        mock_filter.is_match = mock.MagicMock(return_value=True)

        command = columnscommand.ColumnsCommand(mock_context, mock_filter)
        command.execute()

        add_column_call1 = mock.call('Columns')
        add_column_call2 = mock.call('Type')
        add_column_call3 = mock.call('Modifiable')
        add_column_call4 = mock.call('Supported Formats')
        add_column_call5 = mock.call('Example')
        add_column_calls = [add_column_call1, add_column_call2, add_column_call3, add_column_call4, add_column_call5]
        self.assertEqual(add_column_calls, mock_context.mock_table.add_column.mock_calls)

        add_row_calls = []
        add_row_calls.append(mock.call('description', 'string', 'Modifiable', 'desc', 'Move your clothes down on to the lower peg'))
        add_row_calls.append(mock.call('end', 'date', 'Modifiable', 'formatted', '2021-04-17'))
        add_row_calls.append(mock.call('', '', '', 'relative', '-4d'))
        add_row_calls.append(mock.call('entry', 'date', 'Modifiable', 'formatted', '2021-04-17'))
        add_row_calls.append(mock.call('', '', '', 'relative', '-4d'))
        add_row_calls.append(mock.call('id', 'numeric', '', 'number*', '123'))
        
        #add_row_calls.append(mock.call('project', 'string', 'Modifiable', '', ''))
        #add_row_calls.append(mock.call('', '', '', '', 'project1'))
        #add_row_calls.append(mock.call('', '', '', '', 'project2'))

        add_row_calls.append(mock.call('start', 'date', '', 'formatted', '2021-04-17'))
        add_row_calls.append(mock.call('', '', '', 'relative', '-4d'))
        add_row_calls.append(mock.call('status', 'string', 'Modifiable', 'long*', 'Pending'))
        add_row_calls.append(mock.call('', '', '', 'short', 'P'))
        add_row_calls.append(mock.call('wait', 'date', '', 'formatted', '2021-04-17'))
        add_row_calls.append(mock.call('', '', '', 'relative', '-4d'))
        self.assertEqual(add_row_calls, mock_context.mock_table.add_row.mock_calls)

        mock_context.console.print_lines.assert_called()

    def _create_context(self, tasks=None):
        if not tasks:
            tasks = self._create_tasks(3)

        mock_settings = mock.Mock()
        mock_settings.command_done_confirm = False

        mock_storage = mock.Mock()
        mock_storage.delete = mock.MagicMock()
        mock_storage.read_all = mock.MagicMock(return_value=tasks)

        mock_table = mock.Mock()
        mock_table.add_column = mock.MagicMock()
        mock_table.add_row = mock.MagicMock()
        mock_table.create_output = mock.MagicMock(return_value='')

        mock_context = mock.Mock()
        mock_context.create_table = mock.MagicMock(return_value=mock_table)
        mock_context.mock_table = mock_table
        mock_context.settings = mock_settings
        mock_context.storage = mock_storage

        return mock_context

    def _create_tasks(self, count):
        tasks = []
        for index in range(count):
            task = mock.Mock()
            task.annotations = []
            task.attributes = {}
            task.index = index + 1
            task.name = 'task {}'.format(task.index)
            tasks.append(task)
        return tasks


class ColumnsCommandParserTests(unittest.TestCase):
    def test_parse_success(self):
        args = ['all', 'args', 'are', 'ignored']

        mock_filter = mock.Mock()

        mock_filter_factory = mock.Mock()
        mock_filter_factory.parse = mock.MagicMock(return_value=mock_filter)

        mock_context = mock.Mock()
        mock_context.filter_factory = mock_filter_factory
        mock_context.settings = mock.Mock()

        parser = columnscommand.ColumnsCommandParser()
        command = parser.parse(mock_context, args)

        self.assertIsInstance(command, columnscommand.ColumnsCommand)
        self.assertEqual(mock_context, command.context)
