import unittest
from unittest import mock

import commands.shellcommand as shellcommand
import filters.allbatchfilter as allbatchfilter
import filters.confirmfilter as confirmfilter


class ShellTests(unittest.TestCase):
    def test_constructor_handles_null_callback(self):
        with self.assertRaises(ValueError):
            shellcommand.Shell(None)

    def test_constructor_succeeds(self):
        mock_callback = mock.MagicMock()
        shellcommand.Shell(mock_callback)

    def test_exit_command_default(self):
        shell = shellcommand.Shell(mock.MagicMock())
        self.assertEqual('exit', shell.exit_command)

    def test_exit_command_setter(self):
        expected = 'new value'
        shell = shellcommand.Shell(mock.MagicMock())
        shell.exit_command = expected
        self.assertEqual(expected, shell.exit_command)

    def test_prompt_default(self):
        shell = shellcommand.Shell(mock.MagicMock())
        self.assertEqual('> ', shell.prompt)

    def test_prompt_setter(self):
        expected = 'new value'
        shell = shellcommand.Shell(mock.MagicMock())
        shell.prompt = expected
        self.assertEqual(expected, shell.prompt)
    
    def test_enter_succeeds(self):
        prompt = 'new prompt'
        exit_command = 'quit'
        mock_print = mock.MagicMock()
        mock_input = mock.MagicMock()
        mock_input.side_effect = ['test command', exit_command]
        shell = shellcommand.Shell(mock.MagicMock())
        shell.exit_command = exit_command
        shell.prompt = prompt
        with mock.patch('commands.shellcommand.print', mock_print):
            with mock.patch('commands.shellcommand.input', mock_input):
                shell.enter()
        mock_print.assert_called()
        # ensure two prompts then exit
        input_calls = [mock.call(prompt), mock.call(prompt)]
        self.assertEqual(input_calls, mock_input.mock_calls)
    
    def test_enter_handles_callback_exception(self):
        prompt = 'new prompt'
        exit_command = 'exit'
        mock_input = mock.MagicMock()
        mock_input.side_effect = ['test command', exit_command]
        mock_callback = mock.MagicMock()
        mock_callback.side_effect = Exception()
        shell = shellcommand.Shell(mock_callback)
        shell.exit_command = exit_command
        shell.prompt = prompt
        with mock.patch('commands.shellcommand.print', mock.MagicMock()):
            with mock.patch('commands.shellcommand.input', mock_input):
                shell.enter()
        # ensure still prompts after exception
        input_calls = [mock.call(prompt), mock.call(prompt)]
        self.assertEqual(input_calls, mock_input.mock_calls)


class ShellCommandTests(unittest.TestCase):
    def test_constructor_sets_properties(self):
        mock_context = mock.Mock()
        command = shellcommand.ShellCommand(mock_context)
        self.assertEqual(mock_context, command.context)
    
    def test_execute_calls_enter_on_shell(self):
        mock_shell = mock.Mock()
        mock_shell.enter = mock.Mock()
        command = shellcommand.ShellCommand(mock.Mock(), mock_shell)
        command.execute()
        mock_shell.enter.assert_called_once()
    
    def test_handle_command_shell_callback(self):
        command_string = '45 list'
        expected_args = ['45', 'list']
        mock_command = mock.Mock()
        mock_command.execute = mock.MagicMock()
        mock_context = mock.Mock()
        mock_context.command_factory = mock.Mock()
        mock_context.command_factory.get_command = mock.MagicMock(return_value=mock_command)
        command = shellcommand.ShellCommand(mock_context)
        command.handle_command(command_string)
        mock_context.command_factory.get_command.assert_called_once_with(expected_args)
        mock_command.execute.assert_called_once()


class ShellCommandParserTests(unittest.TestCase):
    def test_constructor_succeeds(self):
        shellcommand.ShellCommandParser()

    def test_parse_wrong_command(self):
        args = ['wrong']
        mock_context = mock.Mock()
        command = shellcommand.ShellCommandParser().parse(mock_context, args)
        self.assertEqual(None, command)

    def test_parse_success(self):
        args = ['shell']
        mock_context = mock.Mock()
        mock_context.settings = mock.Mock()
        parser = shellcommand.ShellCommandParser()
        command = parser.parse(mock_context, args)
        self.assertIsInstance(command, shellcommand.ShellCommand)
        self.assertEqual(mock_context, command.context)

    def test_get_usage(self):
        parser = shellcommand.ShellCommandParser()
        self.assertEqual('tasks shell', parser.get_usage())
