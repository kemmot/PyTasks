import unittest
from unittest import mock

import commands.commandfactory as commandfactory
import commandline


class CommandFactoryTests(unittest.TestCase):
    def test_get_command_no_command_specified_and_no_default(self):
        mock_context = mock.Mock()
        mock_context.settings = mock.Mock()
        mock_context.settings.command_default = ''
        factory = commandfactory.CommandFactory(mock_context)
        try:
            args = []
            factory.get_command(args)
            self.fail('Should not have reached this code')
        except commandline.ExitCodeException as ex:
            self.assertEqual(commandline.ExitCodes.no_command_specified_error, ex.exit_code)

    def test_get_command_no_command_specified_with_known_default(self):
        mock_context = mock.Mock()
        mock_context.settings = mock.Mock()
        mock_context.settings.command_default = 'test'

        expected_command = mock.Mock()

        parser = mock.Mock()
        parser.parse = mock.MagicMock(return_value=expected_command)

        factory = commandfactory.CommandFactory(mock_context)
        factory.register_type(parser)
        args = []
        command = factory.get_command(args)
        self.assertEqual(command, expected_command)

    def test_get_command_no_command_specified_with_unknown_default(self):
        mock_context = mock.Mock()
        mock_context.settings = mock.Mock()
        mock_context.settings.command_default = 'test'
        
        factory = commandfactory.CommandFactory(mock_context)
        try:
            args = []
            factory.get_command(args)
            self.fail('Should not have reached this code')
        except commandline.ExitCodeException as ex:
            self.assertEqual(commandline.ExitCodes.unknown_command_error, ex.exit_code)

    def test_get_unknown_command(self):
        mock_storage = mock.Mock()
        factory = commandfactory.CommandFactory(mock_storage)
        try:
            args = ['unknown']
            factory.get_command(args)
            self.fail('Should not have reached this code')
        except commandline.ExitCodeException as ex:
            self.assertEqual(commandline.ExitCodes.unknown_command_error, ex.exit_code)

    def test_get_known_command(self):
        args = ['test']

        expected_command = mock.Mock()

        parser = mock.Mock()
        parser.parse = mock.MagicMock(return_value=expected_command)

        mock_context = mock.Mock()
        factory = commandfactory.CommandFactory(mock_context)
        factory.register_type(parser)

        command = factory.get_command(args)

        self.assertEqual(command, expected_command)
        parser.parse.assert_called_once_with(mock_context, args)

    def test_register_known_parsers_registers(self):
        expected_command = mock.Mock()

        parser = mock.Mock()
        parser.parse = mock.MagicMock(return_value=expected_command)

        mock_storage = mock.Mock()
        factory = commandfactory.CommandFactory(mock_storage)
        factory.register_type(parser)
        command = factory.get_command(['test'])
        self.assertEqual(expected_command, command)
