import unittest
import uuid
from unittest import mock

import commands.infocommand as infocommand
import filters.allbatchfilter as allbatchfilter
import filters.confirmfilter as confirmfilter


class InfoCommandTests(unittest.TestCase):
    def test_constructor_sets_properties(self):
        mock_context = mock.Mock()
        mock_filter = mock.Mock()
        command = infocommand.InfoCommand(mock_context, mock_filter)
        self.assertEqual(mock_context, command.context)
        self.assertEqual(mock_filter, command.filter)

    def test_execute_calls_read_all_on_storage(self):
        mock_filter = mock.Mock()
        mock_filter.filter_items = mock.MagicMock(return_value=self._create_tasks(1))

        mock_context = self._create_context()
        command = infocommand.InfoCommand(mock_context, mock_filter)
        command.execute()

        mock_context.storage.read_all.assert_called_once()

    def test_execute_prints_task_details(self):
        task = self._create_tasks(1)[0]

        mock_filter = mock.Mock()
        mock_filter.filter_items = mock.MagicMock(return_value=[task])

        mock_context = self._create_context()
        command = infocommand.InfoCommand(mock_context, mock_filter)
        
        mock_print = mock.MagicMock()
        with mock.patch('commands.infocommand.print', mock_print):
            command.execute()

        calls = []
        calls.append(mock.call('Name        Value'))
        calls.append(mock.call('ID          {}'.format(task.index)))
        calls.append(mock.call('Description {}'.format(task.name)))
        calls.append(mock.call('Status      {}'.format(task.status)))
        calls.append(mock.call('Entered     {}'.format(task.created)))
        calls.append(mock.call('UUID        {}'.format(task.id_number)))
        self.assertEqual(calls, mock_print.mock_calls)

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
            task.annotations = []
            task.id_number = uuid.uuid4()
            task.index = index + 1
            task.name = 'task {}'.format(task.index)
            tasks.append(task)
        return tasks
