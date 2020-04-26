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
        parser = commandbase.CommandParserBase('base')

        mock_print = mock.MagicMock()
        with mock.patch('commands.commandbase.print', mock_print):
            parser.print_help()

        mock_print.assert_called_with('tasks base')

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
        parser = commandbase.FilterCommandParserBase('base')

        mock_print = mock.MagicMock()
        with mock.patch('commands.commandbase.print', mock_print):
            parser.print_help()

        mock_print.assert_called_with('tasks [filter] base')
