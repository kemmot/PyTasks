import unittest
from unittest import mock
from unittest.mock import MagicMock

import commands.helpcommand as helpcommand


class HelpCommandTests(unittest.TestCase):
    def test_execute_prints_help(self):
        parsers = []
        mock_parser1 = mock.Mock()
        mock_parser1.command_name = 'parser1'
        mock_parser1.print_help = mock.MagicMock()
        parsers.append(mock_parser1)
        mock_parser2 = mock.Mock()
        mock_parser2.command_name = 'parser2'
        mock_parser2.print_help = mock.MagicMock()
        parsers.append(mock_parser2)

        context = mock.Mock()
        context.command_factory = mock.Mock()
        context.command_factory.types = parsers

        command = helpcommand.HelpCommand(context)
        command.execute()

        mock_parser1.print_help.assert_called()
        mock_parser2.print_help.assert_called()


class HelpCommandParserTests(unittest.TestCase):
    def test_parse_success(self):
        args = ['this', 'can', 'be', 'anything']
        mock_context = mock.Mock()
        command = helpcommand.HelpCommandParser().parse(mock_context, args)
        self.assertNotEqual(None, command)
        self.assertIsInstance(command, helpcommand.HelpCommand)
