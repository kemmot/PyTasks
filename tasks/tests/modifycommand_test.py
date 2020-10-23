import unittest
from unittest import mock

import commands.modifycommand as modifycommand
import filters.allbatchfilter as allbatchfilter
import filters.confirmfilter as confirmfilter


class ModifyCommandTests(unittest.TestCase):
    def test_constructor_sets_properties(self):
        mock_context = mock.Mock()
        mock_filter = mock.Mock()
        command = modifycommand.ModifyCommand(mock_context, mock_filter)
        self.assertEqual(mock_context, command.context)
        self.assertEqual(mock_filter, command.filter)

    def test_execute_calls_read_all_on_storage(self):
        mock_context = self._create_context()

        template_task = self._create_tasks(1)[0]
        template_task.name = 'new name'

        mock_filter = mock.MagicMock()
        mock_filter.is_match = mock.MagicMock(return_value=True)

        command = modifycommand.ModifyCommand(mock_context, mock_filter)
        command.template_task = template_task
        command.execute()

        mock_context.storage.read_all.assert_called_once()

    def test_execute_sets_task_name(self):
        tasks = self._create_tasks(3)

        template_task = self._create_tasks(1)[0]
        template_task.name = 'new name'

        mock_context = self._create_context(tasks)

        mock_filter = mock.MagicMock()
        mock_filter.filter_items = mock.MagicMock(return_value=[tasks[1]])

        command = modifycommand.ModifyCommand(mock_context, mock_filter)
        command.template_task = template_task
        command.execute()

        self.assertEqual('new name', tasks[1].name)

    def test_execute_does_not_alter_name_when_not_specified(self):
        tasks = self._create_tasks(3)
        tasks[1].name = 'original name'

        template_task = self._create_tasks(1)[0]
        template_task.name = ''

        mock_context = self._create_context(tasks)

        mock_filter = mock.MagicMock()
        mock_filter.filter_items = mock.MagicMock(return_value=[tasks[1]])

        command = modifycommand.ModifyCommand(mock_context, mock_filter)
        command.template_task = template_task
        command.execute()

        self.assertEqual('original name', tasks[1].name)

    def test_execute_adds_new_attributes(self):
        attribute_name = 'project'
        attribute_value = 'test'
        tasks = self._create_tasks(3)

        template_task = self._create_tasks(1)[0]
        template_task.name = ''
        template_task.attributes[attribute_name] = attribute_value

        mock_context = self._create_context(tasks)

        mock_filter = mock.MagicMock()
        mock_filter.filter_items = mock.MagicMock(return_value=[tasks[1]])

        command = modifycommand.ModifyCommand(mock_context, mock_filter)
        command.template_task = template_task
        command.execute()

        self.assertEqual(1, len(tasks[1].attributes))
        self.assertTrue(attribute_name in tasks[1].attributes)
        self.assertEqual(attribute_value, tasks[1].attributes[attribute_name])

    def test_execute_updates_existing_attributes(self):
        attribute_name = 'project'
        attribute_value = 'test'
        attribute_value2 = 'new value'
        tasks = self._create_tasks(3)
        tasks[1].attributes[attribute_name] = attribute_value

        template_task = self._create_tasks(1)[0]
        template_task.name = ''
        template_task.attributes[attribute_name] = attribute_value2

        mock_context = self._create_context(tasks)

        mock_filter = mock.MagicMock()
        mock_filter.filter_items = mock.MagicMock(return_value=[tasks[1]])

        command = modifycommand.ModifyCommand(mock_context, mock_filter)
        command.template_task = template_task
        command.execute()

        self.assertEqual(1, len(tasks[1].attributes))
        self.assertTrue(attribute_name in tasks[1].attributes)
        self.assertEqual(attribute_value2, tasks[1].attributes[attribute_name])

    def test_execute_calls_update_on_storage(self):
        tasks = self._create_tasks(3)
        mock_context = self._create_context(tasks)

        template_task = self._create_tasks(1)[0]
        template_task.name = 'new name'

        mock_filter = mock.MagicMock()
        mock_filter.filter_items = mock.MagicMock(return_value=[tasks[1]])

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
            task.attributes = {}
            task.index = index + 1
            task.name = 'task {}'.format(task.index)
            tasks.append(task)
        return tasks


class ModifyCommandParserTests(unittest.TestCase):
    def test_get_confirm_filter_no_confirmation(self):
        filter = self.execute_get_confirm_filter(False)
        self.assertIsNone(filter)

    def test_get_confirm_filter_with_confirmation(self):
        filter = self.execute_get_confirm_filter(True)
        self.assertIsNotNone(filter)
        self.assertIsInstance(filter, confirmfilter.ConfirmFilter)
        self.assertIn('Modify', filter.action_name)
        
    def execute_get_confirm_filter(self, with_confirmation):
        mock_context = mock.Mock()
        mock_context.settings = mock.Mock()
        mock_context.settings.command_modify_confirm = with_confirmation

        parser = modifycommand.ModifyCommandParser()
        return parser.get_confirm_filter(mock_context)

    def test_parse_parse_success_with_project_and_priority(self):
        command = self._test_parse_parse_success(False, ['project:test', 'priority:H'])
        self.assertEqual(len(command.template_task.attributes), 2)
        self.assertTrue('project' in command.template_task.attributes)
        self.assertEqual(command.template_task.attributes['project'], 'test')
        self.assertTrue('priority' in command.template_task.attributes)
        self.assertEqual(command.template_task.attributes['priority'], 'H')

    def _test_parse_parse_success(self, with_confirmation, extra_args=None):
        args = ['new', 'name']
        if extra_args:
            for extra_arg in extra_args:
                args.append(extra_arg)

        mock_context = mock.Mock()
        parser = modifycommand.ModifyCommandParser()
        command = parser.parse(mock_context, args)

        self.assertIsInstance(command, modifycommand.ModifyCommand)
        self.assertEqual(mock_context, command.context)
        self.assertIsNotNone(command.template_task)
        self.assertEqual(command.template_task.name, 'new name')
        return command

    def test_get_usage(self):
        parser = modifycommand.ModifyCommandParser()
        self.assertEqual('tasks [filter] modify [attribute:value]', parser.get_usage())
