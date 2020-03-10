import unittest
from unittest import mock

import commands.modifycommand as modifycommand


class ModifyCommandTests(unittest.TestCase):
    def test_constructor_sets_properties(self):
        mock_context = mock.Mock()
        mock_filter = mock.Mock()
        command = modifycommand.ModifyCommand(mock_context, mock_filter)
        self.assertEqual(mock_context, command.context)
        self.assertEqual(mock_filter, command.filter)

    def test_execute_calls_read_all_on_storage(self):
        tasks = self._create_tasks(3)
        mock_context = self._create_context(tasks)

        mock_filter = mock.MagicMock()
        mock_filter.is_match = mock.MagicMock(return_value=True)

        template_task = mock.Mock()
        template_task.name = 'new name'

        command = modifycommand.ModifyCommand(mock_context, mock_filter)
        command.template_task = template_task
        command.execute()

        mock_context.storage.read_all.assert_called_once()

    def test_execute_sets_task_name(self):
        tasks = self._create_tasks(3)
        mock_context = self._create_context(tasks)

        mock_filter = mock.MagicMock()
        mock_filter.filter_items = mock.MagicMock(return_value=[tasks[1]])

        template_task = mock.Mock()
        template_task.name = 'new name'

        command = modifycommand.ModifyCommand(mock_context, mock_filter)
        command.template_task = template_task
        command.execute()

        self.assertEqual('new name', tasks[1].name)

    def test_execute_calls_update_on_storage(self):
        tasks = self._create_tasks(3)
        mock_context = self._create_context(tasks)

        mock_filter = mock.MagicMock()
        mock_filter.filter_items = mock.MagicMock(return_value=[tasks[1]])

        template_task = mock.Mock()
        template_task.name = 'new name'

        command = modifycommand.ModifyCommand(mock_context, mock_filter)
        command.template_task = template_task
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
            task.index = index + 1
            task.name = 'task {}'.format(task.index)
            tasks.append(task)
        return tasks


class ModifyCommandParserTests(unittest.TestCase):
    def test_parse_wrong_command(self):
        args = ['wrong']
        mock_context = mock.Mock()
        mock_filter_factory = mock.Mock()
        command = modifycommand.ModifyCommandParser().parse(mock_context, mock_filter_factory, args)
        self.assertEqual(None, command)

    def test_parse_no_filter(self):
        args = ['modify']
        mock_context = mock.Mock()
        mock_filter_factory = mock.Mock()
        parser = modifycommand.ModifyCommandParser()
        result = parser.parse(mock_context, mock_filter_factory, args)
        self.assertIsNone(result)

    def test_parse_no_filter_parsed(self):
        args = ['text', 'modify', 'new name']
        mock_context = mock.Mock()
        mock_filter_factory = mock.Mock()
        mock_filter_factory.parse = mock.MagicMock()
        mock_filter_factory.parse.side_effect = Exception
        with self.assertRaises(Exception):
            modifycommand.ModifyCommandParser().parse(mock_context, mock_filter_factory, args)

    def test_parse_parse_success(self):
        args = ['2', 'modify', 'new name']
        mock_context = mock.Mock()
        mock_filter_factory = mock.Mock()
        mock_filter = mock.Mock()
        mock_filter_factory.parse = mock.MagicMock(return_value=mock_filter)
        parser = modifycommand.ModifyCommandParser()
        command = parser.parse(mock_context, mock_filter_factory, args)
        self.assertIsInstance(command, modifycommand.ModifyCommand)
        self.assertEqual(mock_context, command.context)
        self.assertEqual(mock_filter, command.filter)
        self.assertIsNotNone(command.template_task)
        self.assertEqual(command.template_task.name, 'new name')