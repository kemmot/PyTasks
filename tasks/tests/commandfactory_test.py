import unittest
from unittest import mock
from unittest.mock import MagicMock
import uuid

import commandfactory
import entities


class CommandFactoryTests(unittest.TestCase):
    def test_get_unknown_command(self):
        args = mock.Mock()
        args.command = 'unknown'
        factory = commandfactory.CommandFactory('filename')
        with self.assertRaises(Exception):
            factory.get_command(args)

    def test_get_known_command(self):
        args = mock.Mock()
        args.command = 'add'

        expected_command = mock.Mock()

        parser = mock.Mock()
        parser.get_name = mock.MagicMock(return_value=args.command)
        parser.parse = mock.MagicMock(return_value=expected_command)

        storage = mock.Mock()
        factory = commandfactory.CommandFactory(storage)
        factory.register_parser(parser)

        command = factory.get_command(args)

        self.assertEqual(command, expected_command)
        parser.get_name.assert_called_once()
        parser.parse.assert_called_once_with(storage, args)

    def test_register_known_parsers_registers(self):
        args = mock.Mock()
        args.command = 'testcommand'

        expected_command = mock.Mock()

        parser = mock.Mock()
        parser.get_name = mock.MagicMock(return_value=args.command)
        parser.parse = mock.MagicMock(return_value=expected_command)

        storage = mock.Mock()
        factory = commandfactory.CommandFactory(storage)
        factory.register_parser(parser)
        command = factory.get_command(args)
        self.assertEqual(expected_command, command)
