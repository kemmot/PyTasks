import unittest
from unittest import mock
from unittest.mock import MagicMock

import commands.helpcommand as helpcommand


class HelpCommandParserTests(unittest.TestCase):
    def test_parse_wrong_command(self):
        args = ['wrong']
        mock_context = mock.Mock()
        command = helpcommand.HelpCommandParser().parse(mock_context, args)
        self.assertEqual(None, command)

    def test_parse_no_filter(self):
        args = ['help']
        mock_context = mock.Mock()
        command = helpcommand.HelpCommandParser().parse(mock_context, args)
        self.assertNotEqual(None, command)
        self.assertIsInstance(command, helpcommand.HelpCommand)

