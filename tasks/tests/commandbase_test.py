import unittest
from unittest import mock

import commands.commandbase as commandbase


class CommandBaseTests(unittest.TestCase):
    def test_execute_errors(self):
        mock_storage = mock.MagicMock()
        command = commandbase.CommandBase(mock_storage)
        with self.assertRaises(Exception):
            command.execute()


class CommandParserBaseTests(unittest.TestCase):
    def test_constructor_args(self):
        command_name = 'command name'
        parser = commandbase.CommandParserBase(command_name)
        self.assertEqual(command_name, parser.command_name)

    def test_parse_errors(self):
        parser = commandbase.CommandParserBase('command name')
        with self.assertRaises(Exception):
            parser.parse(mock.Mock(), [])

    def test_print_help(self):
        mock_console = mock.Mock()
        mock_console.print = mock.MagicMock()

        parser = commandbase.CommandParserBase('base')
        parser.print_help(mock_console)

        mock_console.print.assert_called_with('tasks base')


class FilterCommandParserBaseTests(unittest.TestCase):
    def test_constructor_args(self):
        command_name = 'command name'
        parser = commandbase.FilterCommandParserBase(command_name)
        self.assertEqual(command_name, parser.command_name)

    def test_parse_errors(self):
        parser = commandbase.FilterCommandParserBase('command name')
        with self.assertRaises(Exception):
            parser.parse(mock.Mock(), [])

    def test_print_help(self):
        mock_console = mock.Mock()
        mock_console.print = mock.MagicMock()

        parser = commandbase.FilterCommandParserBase('base')
        parser.print_help(mock_console)

        mock_console.print.assert_called_with('tasks [filter] base')
