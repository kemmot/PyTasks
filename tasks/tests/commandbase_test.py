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
    def test_parse_errors(self):
        mock_storage = mock.Mock()
        mock_filter_factory = mock.Mock()
        parser = commandbase.CommandParserBase()
        args = []
        with self.assertRaises(Exception):
            parser.parse(mock_storage, mock_filter_factory, args)
