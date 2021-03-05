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
    def test_get_confirm_filter_no_confirmation(self):
        confirm_filter = self.execute_get_confirm_filter(False)
        self.assertIsNone(confirm_filter)

    def test_get_confirm_filter_with_confirmation(self):
        confirm_filter = self.execute_get_confirm_filter(True)
        self.assertIsNotNone(confirm_filter)
        self.assertIsInstance(confirm_filter, confirmfilter.ConfirmFilter)
        self.assertIn('Stop', confirm_filter.action_name)

    def execute_get_confirm_filter(self, with_confirmation):
        mock_context = mock.Mock()
        mock_context.settings = mock.Mock()
        mock_context.settings.command_stop_confirm = with_confirmation

        parser = stopcommand.StopCommandParser()
        return parser.get_confirm_filter(mock_context)

    def test_get_usage(self):
        parser = stopcommand.StopCommandParser()
        self.assertEqual('tasks [filter] stop', parser.get_usage())
