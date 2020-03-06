import unittest
from unittest import mock

import commands.donecommand as donecommand


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
        mock_filter.is_match = mock.Mock()
        mock_filter.is_match.side_effect = [False, True, False]

        command = donecommand.DoneCommand(mock_context, mock_filter)
        command.execute()

        mock_context.storage.read_all.assert_called_once()
        mock_context.storage.delete.assert_called_once_with(tasks[1])

    def test_execute_does_not_prompt_for_zero_deletions(self):
        mock_filter = mock.MagicMock()
        mock_filter.is_match = mock.MagicMock(return_value=False)
        self._test_execute_prompts_when_confgured_to(mock_filter, None)

    def test_execute_does_not_prompt_when_not_configured_to(self):
        mock_filter = mock.MagicMock()
        mock_filter.is_match = mock.MagicMock(return_value=True)
        self._test_execute_prompts_when_confgured_to(mock_filter, None, False)

    def test_execute_prompts_before_single_deletion_when_configured_to(self):
        mock_filter = mock.MagicMock()
        mock_filter.is_match = mock.Mock()
        mock_filter.is_match.side_effect = [False, True, False]
        self._test_execute_prompts_when_confgured_to(mock_filter, 'Mark task as done?... ID: 2, name: task 2')

    def test_execute_prompts_before_multiple_deletion_when_configured_to(self):
        mock_filter = mock.MagicMock()
        mock_filter.is_match = mock.MagicMock(return_value=True)
        self._test_execute_prompts_when_confgured_to(mock_filter, 'Mark task(s) as done?... 3 tasks')

    def _test_execute_prompts_when_confgured_to(self, mock_filter, message, prompt=True):
        tasks = self._create_tasks(3)
        mock_context = self._create_context(tasks)
        mock_context.settings.command_done_confirm = prompt

        command = donecommand.DoneCommand(mock_context, mock_filter)

        mock_print = mock.MagicMock()
        with mock.patch('commands.donecommand.print', mock_print):
            command.execute()
        
        if not message:
            mock_print.assert_not_called()
        else:
            mock_print.assert_called_once_with(message)
        
    def test_execute_negative_confirmation_does_not_change_task(self):
        pass
        
    def test_execute_positive_confirmation_does_change_task(self):
        pass

    def _create_context(self, tasks):
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

    def test_parse_no_filter(self):
        args = ['done']
        mock_context = mock.Mock()
        mock_filter_factory = mock.Mock()
        parser = donecommand.DoneCommandParser()
        result = parser.parse(mock_context, mock_filter_factory, args)
        self.assertIsNone(result)

    def test_parse_no_filter_parsed(self):
        args = ['text', 'done']
        mock_context = mock.Mock()
        mock_filter_factory = mock.Mock()
        mock_filter_factory.parse = mock.MagicMock()
        mock_filter_factory.parse.side_effect = Exception
        with self.assertRaises(Exception):
            donecommand.DoneCommandParser().parse(mock_context, mock_filter_factory, args)

    def test_parse_parse_success(self):
        args = ['2', 'done']
        mock_context = mock.Mock()
        mock_filter_factory = mock.Mock()
        mock_filter = mock.Mock()
        mock_filter_factory.parse = mock.MagicMock(return_value=mock_filter)
        parser = donecommand.DoneCommandParser()
        command = parser.parse(mock_context, mock_filter_factory, args)
        self.assertIsInstance(command, donecommand.DoneCommand)
        self.assertEqual(mock_context, command.context)
        self.assertEqual(mock_filter, command.filter)
