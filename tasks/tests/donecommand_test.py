import unittest
from unittest import mock

import commands.donecommand as donecommand
import filters.allbatchfilter as allbatchfilter
import filters.confirmfilter as confirmfilter

class DoneCommandTests(unittest.TestCase):
    def test_constructor_sets_properties(self):
        mock_context = mock.Mock()
        mock_filter = mock.Mock()
        command = donecommand.DoneCommand(mock_context, mock_filter)
        self.assertEqual(mock_context, command.context)
        self.assertEqual(mock_filter, command.filter)

    def test_execute_calls_delete_on_storage(self):
        tasks = self._create_tasks(3)
        mock_context = self._create_context(tasks)

        mock_filter = mock.MagicMock()
        mock_filter.filter_items = mock.MagicMock(return_value=[tasks[1]])

        command = donecommand.DoneCommand(mock_context, mock_filter)
        command.execute()

        mock_context.storage.read_all.assert_called_once()
        mock_context.storage.delete.assert_called_once_with(tasks[1])

    def _create_context(self, tasks=None):
        if not tasks:
            tasks = self._create_tasks(3)

        mock_settings = mock.Mock()
        mock_settings.command_done_confirm = False
        
        mock_storage = mock.Mock()
        mock_storage.delete = mock.MagicMock()
        mock_storage.read_all = mock.MagicMock(return_value=tasks)

        mock_context = mock.Mock()
        mock_context.settings = mock_settings
        mock_context.storage = mock_storage

        return mock_context

    def _create_tasks(self, count):
        tasks = []
        for index in range(count):
            task = mock.Mock()
            task.index = index + 1
            task.name = 'task {}'.format(task.index)
            tasks.append(task)
        return tasks


class DoneCommandParserTests(unittest.TestCase):
    def test_parse_wrong_command(self):
        args = ['wrong']
        mock_context = mock.Mock()
        mock_filter_factory = mock.Mock()
        command = donecommand.DoneCommandParser().parse(mock_context, mock_filter_factory, args)
        self.assertEqual(None, command)

    def test_parse_no_filter_specified(self):
        args = ['done']
        mock_context = mock.Mock()
        mock_filter_factory = mock.Mock()
        parser = donecommand.DoneCommandParser()
        result = parser.parse(mock_context, mock_filter_factory, args)
        self.assertIsNone(result)

    def test_parse_filter_not_found(self):
        args = ['text', 'done']
        mock_context = mock.Mock()
        mock_filter_factory = mock.Mock()
        mock_filter_factory.parse = mock.MagicMock()
        mock_filter_factory.parse.side_effect = Exception
        with self.assertRaises(Exception):
            donecommand.DoneCommandParser().parse(mock_context, mock_filter_factory, args)

    def test_parse_parse_success_no_confirmation(self):
        self._test_parse_parse_success(False)

    def test_parse_parse_success_with_confirmation(self):
        self._test_parse_parse_success(True)
        
    def _test_parse_parse_success(self, with_confirmation):
        args = ['2', 'done']
        mock_context = mock.Mock()
        mock_context.settings = mock.Mock()
        mock_context.settings.command_done_confirm = with_confirmation

        mock_filter_factory = mock.Mock()
        mock_filter = mock.Mock()
        mock_filter_factory.parse = mock.MagicMock(return_value=mock_filter)

        parser = donecommand.DoneCommandParser()
        command = parser.parse(mock_context, mock_filter_factory, args)

        self.assertIsInstance(command, donecommand.DoneCommand)
        self.assertEqual(mock_context, command.context)
        self.assertIsInstance(command.filter, allbatchfilter.AllBatchFilter)
        self.assertEqual(mock_filter, command.filter._filters[0])

        if with_confirmation:
            self.assertEqual(2, len(command.filter._filters))
            self.assertIsInstance(command.filter._filters[1], confirmfilter.ConfirmFilter)
            self.assertIn('Mark as done', command.filter._filters[1].action_name)
        else:
            self.assertEqual(1, len(command.filter._filters))
