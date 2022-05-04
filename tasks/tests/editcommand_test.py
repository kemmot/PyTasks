import unittest
from unittest import mock

import commands.editcommand as editcommand
import filters.confirmfilter as confirmfilter


class EditCommandTests(unittest.TestCase):
    def test_constructor_sets_properties(self):
        mock_context = mock.Mock()
        mock_filter = mock.Mock()
        command = editcommand.EditCommand(mock_context, mock_filter)
        self.assertEqual(mock_context, command.context)
        self.assertEqual(mock_filter, command.filter)

'''
    def test_execute_calls_delete_on_storage(self):
        tasks = self._create_tasks(3)
        mock_context = self._create_context(tasks)

        mock_filter = mock.MagicMock()
        mock_filter.filter_items = mock.MagicMock(return_value=[tasks[1]])

        command = editcommand.EditCommand(mock_context, mock_filter)
        command.execute()

        mock_context.storage.read_all.assert_called_once()
        tasks[0].end.assert_not_called()
        tasks[1].end.assert_called_once()
        tasks[2].end.assert_not_called()
        expected = []
        expected.append(tasks[1])
        mock_context.storage.update.assert_called_once_with(expected)

    def _create_context(self, tasks=None):
        if not tasks:
            tasks = self._create_tasks(3)

        mock_settings = mock.Mock()
        mock_settings.command_done_confirm = False

        mock_storage = mock.Mock()
        mock_storage.update = mock.MagicMock()
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
            task.end = mock.MagicMock()
            tasks.append(task)
        return tasks
'''


class EditCommandParserTests(unittest.TestCase):
    def test_parse_success(self):
        mock_context = mock.Mock()
        command = editcommand.EditCommandParser().parse(mock_context, [])
        self.assertIsInstance(command, editcommand.EditCommand)
        self.assertEqual(mock_context, command.context)
