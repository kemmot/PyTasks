import unittest
from unittest import mock

import commandfactory
import commandline


class CommandFactoryTests(unittest.TestCase):
    def test_get_command_no_command_specified(self):
        args = []
        factory = commandfactory.CommandFactory('filename')
        try:
            factory.get_command(args)
            self.fail('Should not have reached this code')
        except commandline.ExitCodeException as ex:
            self.assertEqual(commandline.ExitCodes.no_command_specified_error, ex.exit_code)

    def test_get_unknown_command(self):
        args = ['unknown']
        factory = commandfactory.CommandFactory('filename')
        try:
            factory.get_command(args)
            self.fail('Should not have reached this code')
        except commandline.ExitCodeException as ex:
            self.assertEqual(commandline.ExitCodes.unknown_command_error, ex.exit_code)

    def test_get_known_command(self):
        args = ['test']

        expected_command = mock.Mock()

        parser = mock.Mock()
        parser.parse = mock.MagicMock(return_value=expected_command)

        storage = mock.Mock()
        factory = commandfactory.CommandFactory(storage)
        factory.register_parser(parser)

        command = factory.get_command(args)

        self.assertEqual(command, expected_command)
        parser.parse.assert_called_once_with(storage, args)

    def test_register_known_parsers_registers(self):
        expected_command = mock.Mock()

        parser = mock.Mock()
        parser.parse = mock.MagicMock(return_value=expected_command)

        storage = mock.Mock()
        factory = commandfactory.CommandFactory(storage)
        factory.register_parser(parser)
        command = factory.get_command(['test'])
        self.assertEqual(expected_command, command)
