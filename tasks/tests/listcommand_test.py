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

    def test_execute_prints_table(self):
        tasks = []
        tasks.append(mock.Mock())
        tasks.append(mock.Mock())
        tasks.append(mock.Mock())
        tasks.append(mock.Mock())

        tasks[1].attributes = {}
        tasks[1].attributes['project'] = 'test'
        tasks[1].index = 2
        tasks[1].is_ended = False
        tasks[1].name = 'some name'
        tasks[1].is_ended = False
        tasks[1].is_waiting = False
        tasks[1].status = 'this status'

        tasks[2].attributes = {}
        tasks[2].is_ended = False
        tasks[2].is_waiting = True

        tasks[3].attributes = {}
        tasks[3].is_ended = True
        tasks[3].is_waiting = False

        mock_context = self._create_mock_context(tasks)

        mock_filter = mock.Mock()
        mock_filter.filter_items = mock.MagicMock(return_value=[tasks[1], tasks[2], tasks[3]])

        command = listcommand.ListTaskCommand(mock_context, mock_filter)
        command.execute()

        mock_context.console.print_table.assert_called()
        call_args = mock_context.console.print_table.mock_calls[0].args
        table = call_args[0]
        self.assertEqual(7, len(table.columns), 'Column count incorrect')
        self.assertEqual('id', table.columns[0], 'Column label incorrect')
        self.assertEqual('status', table.columns[1], 'Column label incorrect')
        self.assertEqual('description', table.columns[2], 'Column label incorrect')
        self.assertEqual('start', table.columns[3], 'Column label incorrect')
        self.assertEqual('wait', table.columns[4], 'Column label incorrect')
        self.assertEqual('project', table.columns[5], 'Column label incorrect')
        self.assertEqual('does_not_exist', table.columns[6], 'Column label incorrect')
        
        # check that only the one not ended, not waiting, tasks is displayed
        self.assertEqual(1, len(table.rows), 'Row count incorrect')

        # test standard columns
        self.assertEqual('2', table.rows[0][0])
        self.assertEqual('this status', table.rows[0][1])
        self.assertEqual('some name', table.rows[0][2])

        # test dates
        #self.assertEqual('', table.rows[0][3])
        #self.assertEqual('', table.rows[0][4])

        # test custom properties
        self.assertEqual('test', table.rows[0][5])

        # test missing columns
        self.assertEqual('', table.rows[0][6])

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
        mock_console.print_table = mock.MagicMock()

        mock_storage = mock.MagicMock()
        mock_storage.read_all = MagicMock(return_value=tasks)

        mock_context = mock.Mock()
        mock_context.console = mock_console
        mock_context.create_table = mock.MagicMock(return_value=mock_table)
        mock_context.storage = mock_storage
        mock_context.mock_table = mock_table

        mock_context.settings.report_list_columns = 'id,status,description,start,wait,project,does_not_exist'

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
