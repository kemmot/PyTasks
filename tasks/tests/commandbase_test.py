import unittest
from unittest import mock

import commands.commandbase as commandbase


class CommandBaseTests(unittest.TestCase):
    def test_execute_errors(self):
        storage = mock.MagicMock()
        command = commandbase.CommandBase(storage)
        with self.assertRaises(Exception):
            command.execute()


class CommandParserBaseTests(unittest.TestCase):
    def test_get_name_errors(self):
        parser = commandbase.CommandParserBase()
        with self.assertRaises(Exception):
            parser.get_name()

    def test_parse_errors(self):
        parser = commandbase.CommandParserBase()
        with self.assertRaises(Exception):
            parser.parse(mock.Mock(), mock.Mock())
