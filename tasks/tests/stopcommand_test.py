import unittest
from unittest import mock

import commands.stopcommand as stopcommand
import filters.allbatchfilter as allbatchfilter
import filters.confirmfilter as confirmfilter


class StopCommandTests(unittest.TestCase):
    def test_constructor_sets_properties(self):
        mock_context = mock.Mock()
        mock_filter = mock.Mock()
        command = stopcommand.StopCommand(mock_context, mock_filter)
        self.assertEqual(mock_context, command.context)
        self.assertEqual(mock_filter, command.filter)

    def test_execute_calls_read_all_on_storage(self):
        mock_context = self._create_context()

        mock_filter = mock.MagicMock()
        mock_filter.is_match = mock.MagicMock(return_value=True)

        command = stopcommand.StopCommand(mock_context, mock_filter)
        command.execute()

        mock_context.storage.read_all.assert_called_once()

    def test_execute_clears_task_started_time(self):
        tasks = self._create_tasks(3)
        tasks[1].start = mock.MagicMock()

        mock_context = self._create_context(tasks)

        mock_filter = mock.MagicMock()
        mock_filter.filter_items = mock.MagicMock(return_value=[tasks[1]])

        command = stopcommand.StopCommand(mock_context, mock_filter)
        command.execute()

        tasks[1].stop.assert_called_once()

    def test_execute_calls_update_on_storage(self):
        tasks = self._create_tasks(3)
        mock_context = self._create_context(tasks)

        mock_filter = mock.MagicMock()
        mock_filter.filter_items = mock.MagicMock(return_value=[tasks[1]])

        command = stopcommand.StopCommand(mock_context, mock_filter)
        command.execute()

        mock_context.storage.update.assert_called_once_with([tasks[1]])

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
            task.attributes = {}
            task.index = index + 1
            task.name = 'task {}'.format(task.index)
            tasks.append(task)
        return tasks


class StopCommandParserTests(unittest.TestCase):
    def test_parse_wrong_command(self):
        args = ['wrong']
        mock_context = mock.Mock()
        command = stopcommand.StopCommandParser().parse(mock_context, args)
        self.assertEqual(None, command)

    def test_parse_no_filter(self):
        args = ['stop']
        mock_context = mock.Mock()
        parser = stopcommand.StopCommandParser()
        result = parser.parse(mock_context, args)
        self.assertIsNone(result)

    def test_parse_no_filter_parsed(self):
        args = ['text', 'stop']

        mock_filter_factory = mock.Mock()
        mock_filter_factory.parse = mock.MagicMock()
        mock_filter_factory.parse.side_effect = Exception

        mock_context = mock.Mock()
        mock_context.filter_factory = mock_filter_factory

        with self.assertRaises(Exception):
            stopcommand.StopCommandParser().parse(mock_context, args)

    def test_parse_parse_success_no_confirmation(self):
        self._test_parse_parse_success(False)

    def test_parse_parse_success_with_confirmation(self):
        self._test_parse_parse_success(True)

    def _test_parse_parse_success(self, with_confirmation):
        args = ['2', 'stop']

        mock_filter_factory = mock.Mock()
        mock_filter = mock.Mock()
        mock_filter_factory.parse = mock.MagicMock(return_value=mock_filter)

        mock_context = mock.Mock()
        mock_context.settings = mock.Mock()
        mock_context.settings.command_start_confirm = with_confirmation
        mock_context.filter_factory = mock_filter_factory

        parser = stopcommand.StopCommandParser()
        command = parser.parse(mock_context, args)

        self.assertIsInstance(command, stopcommand.StopCommand)
        self.assertEqual(mock_context, command.context)
        self.assertIsInstance(command.filter, allbatchfilter.AllBatchFilter)
        self.assertEqual(mock_filter, command.filter._filters[0])

        if with_confirmation:
            self.assertEqual(2, len(command.filter._filters))
            self.assertIsInstance(command.filter._filters[1], confirmfilter.ConfirmFilter)
            self.assertIn('Stop', command.filter._filters[1].action_name)
        else:
            self.assertEqual(1, len(command.filter._filters))

        return command

    def test_get_usage(self):
        parser = stopcommand.StopCommandParser()
        self.assertEqual('tasks [filter] stop', parser.get_usage())