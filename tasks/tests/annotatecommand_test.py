import unittest
from unittest import mock

import commands.annotatecommand as annotatecommand
import filters.allbatchfilter as allbatchfilter
import filters.confirmfilter as confirmfilter


class AnnotateCommandTests(unittest.TestCase):
    def test_constructor_sets_properties(self):
        mock_context = mock.Mock()
        mock_filter = mock.Mock()
        command = annotatecommand.AnnotateCommand(mock_context, mock_filter)
        self.assertEqual(mock_context, command.context)
        self.assertEqual(mock_filter, command.filter)

    def test_execute_calls_read_all_on_storage(self):
        tasks = self._create_tasks(3)
        mock_context = self._create_context(tasks)

        mock_filter = mock.MagicMock()
        mock_filter.is_match = mock.MagicMock(return_value=True)

        command = annotatecommand.AnnotateCommand(mock_context, mock_filter)
        command.message = 'message'
        command.execute()

        mock_context.storage.read_all.assert_called_once()

    def test_execute_adds_annotation(self):
        tasks = self._create_tasks(3)
        mock_context = self._create_context(tasks)

        mock_filter = mock.MagicMock()
        mock_filter.filter_items = mock.MagicMock(return_value=[tasks[1]])

        command = annotatecommand.AnnotateCommand(mock_context, mock_filter)
        command.message = 'message'
        command.execute()

        self.assertEqual(1, len(tasks[1].annotations))
        self.assertEqual('message', tasks[1].annotations[0].message)

    def test_execute_calls_update_on_storage(self):
        tasks = self._create_tasks(3)
        mock_context = self._create_context(tasks)

        mock_filter = mock.MagicMock()
        mock_filter.filter_items = mock.MagicMock(return_value=[tasks[1]])

        command = annotatecommand.AnnotateCommand(mock_context, mock_filter)
        command.message = 'message'
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
            task.annotations = []
            task.index = index + 1
            task.name = 'task {}'.format(task.index)
            tasks.append(task)
        return tasks


class AnnotateCommandParserTests(unittest.TestCase):
    def test_get_confirm_filter_no_confirmation(self):
        filter = self.execute_get_confirm_filter(False)
        self.assertIsNone(filter)

    def test_get_confirm_filter_with_confirmation(self):
        filter = self.execute_get_confirm_filter(True)
        self.assertIsNotNone(filter)
        self.assertIsInstance(filter, confirmfilter.ConfirmFilter)
        self.assertIn('Annotate', filter.action_name)
        
    def execute_get_confirm_filter(self, with_confirmation):
        mock_context = mock.Mock()
        mock_context.settings = mock.Mock()
        mock_context.settings.command_annotate_confirm = with_confirmation

        parser = annotatecommand.AnnotateCommandParser()
        return parser.get_confirm_filter(mock_context)

    def test_parse_no_message(self):
        mock_context = mock.Mock()
        parser = annotatecommand.AnnotateCommandParser()
        with self.assertRaises(Exception):
            parser.parse(mock_context, [])
        
    def test_parse_success(self):
        args = ['this', 'is', 'a', 'multi-word', 'message']

        mock_filter = mock.Mock()

        mock_filter_factory = mock.Mock()
        mock_filter_factory.parse = mock.MagicMock(return_value=mock_filter)

        mock_context = mock.Mock()
        mock_context.filter_factory = mock_filter_factory
        mock_context.settings = mock.Mock()

        parser = annotatecommand.AnnotateCommandParser()
        command = parser.parse(mock_context, args)

        self.assertIsInstance(command, annotatecommand.AnnotateCommand)
        self.assertEqual(mock_context, command.context)
        self.assertEqual(command.message, 'this is a multi-word message')
