import datetime
import unittest
from unittest import mock

import commands.annotatecommand as annotatecommand
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

    def test_execute_adds_annotation_without_date(self):
        test_start_time = datetime.datetime.now()
        tasks = self._create_tasks(3)
        mock_context = self._create_context(tasks)

        mock_filter = mock.MagicMock()
        mock_filter.filter_items = mock.MagicMock(return_value=[tasks[1]])

        command = annotatecommand.AnnotateCommand(mock_context, mock_filter)
        command.message = 'message'
        command.execute()

        test_end_time = datetime.datetime.now()
        self.assertEqual(1, len(tasks[1].annotations))
        self.assertEqual('message', tasks[1].annotations[0].message)
        self.assertGreaterEqual(tasks[1].annotations[0].created, test_start_time)
        self.assertLessEqual(tasks[1].annotations[0].created, test_end_time)

    def test_execute_adds_annotation_with_date(self):
        tasks = self._create_tasks(3)
        mock_context = self._create_context(tasks)

        mock_filter = mock.MagicMock()
        mock_filter.filter_items = mock.MagicMock(return_value=[tasks[1]])

        annotation_created_date = datetime.datetime(2019, 1, 1)
        command = annotatecommand.AnnotateCommand(mock_context, mock_filter)
        command.created = annotation_created_date
        command.message = 'message'
        command.execute()

        self.assertEqual(1, len(tasks[1].annotations))
        self.assertEqual('message', tasks[1].annotations[0].message)
        self.assertEqual(annotation_created_date, tasks[1].annotations[0].created)

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
        confirm_filter = self.execute_get_confirm_filter(False)
        self.assertIsNone(confirm_filter)

    def test_get_confirm_filter_with_confirmation(self):
        confirm_filter = self.execute_get_confirm_filter(True)
        self.assertIsNotNone(confirm_filter)
        self.assertIsInstance(confirm_filter, confirmfilter.ConfirmFilter)
        self.assertIn('Annotate', confirm_filter.action_name)

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

    def test_parse_success_with_created_date(self):
        args = ['this', 'is', 'a', 'multi-word', 'message', 'created:2021-01-01']

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
        self.assertEqual(command.created, datetime.datetime(2021, 1, 1))
        self.assertEqual(command.message, 'this is a multi-word message')

    def test_parse_duplicate_attribute(self):
        args = ['this', 'is', 'a', 'multi-word', 'message', \
            'created:2021-01-01', 'created:2021-01-02']

        mock_filter = mock.Mock()

        mock_filter_factory = mock.Mock()
        mock_filter_factory.parse = mock.MagicMock(return_value=mock_filter)

        mock_context = mock.Mock()
        mock_context.filter_factory = mock_filter_factory
        mock_context.settings = mock.Mock()

        parser = annotatecommand.AnnotateCommandParser()
        with self.assertRaises(Exception):
            parser.parse(mock_context, args)

    def test_parse_invalid_created_attribute(self):
        args = ['this', 'is', 'a', 'multi-word', 'message', 'created:baddate']

        mock_filter = mock.Mock()

        mock_filter_factory = mock.Mock()
        mock_filter_factory.parse = mock.MagicMock(return_value=mock_filter)

        mock_context = mock.Mock()
        mock_context.filter_factory = mock_filter_factory
        mock_context.settings = mock.Mock()

        parser = annotatecommand.AnnotateCommandParser()
        with self.assertRaises(Exception):
            parser.parse(mock_context, args)

    def test_parse_unknown_attribute(self):
        args = ['this', 'is', 'a', 'multi-word', 'message', 'invalid:wobbly']

        mock_filter = mock.Mock()

        mock_filter_factory = mock.Mock()
        mock_filter_factory.parse = mock.MagicMock(return_value=mock_filter)

        mock_context = mock.Mock()
        mock_context.filter_factory = mock_filter_factory
        mock_context.settings = mock.Mock()

        parser = annotatecommand.AnnotateCommandParser()
        with self.assertRaises(Exception):
            parser.parse(mock_context, args)
