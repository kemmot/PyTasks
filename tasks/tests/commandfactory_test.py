import unittest
from unittest import mock

import commands.commandfactory as commandfactory
import commandline


class CommandFactoryTests(unittest.TestCase):
    pass


class ParsedCommandTests(unittest.TestCase):
    def test_arguments_getter(self):
        args = ['one', 'two']
        factory = commandfactory.ParsedCommand()
        for arg in args: factory.arguments.append(arg)
        self.assertEqual(args, factory.arguments)
    
    def test_get_verb_zero(self):
        with self.assertRaises(Exception):
            self._get_get_verb_value_test('f1 f2 c1 c2', 'va')

    def test_get_verb_single(self):
        self._get_get_verb_value_test('f1 f2 v1 c1 c2', 'v1')

    def test_get_verb_multiple(self):
        self._get_get_verb_value_test('f1 va vb c1 c2', 'va')

    def test_get_command_argument_values_zero(self):
        self._get_command_argument_values_test('f1 f2 v1', [])

    def test_get_command_argument_values_single(self):
        self._get_command_argument_values_test('f1 f2 v1 c1', ['c1'])

    def test_get_command_argument_values_multiple(self):
        self._get_command_argument_values_test('f1 f2 v1 c1 c2', ['c1', 'c2'])

    def test_get_filter_argument_values_zero(self):
        self._get_filter_argument_values_test('v1 c1 c2', [])

    def test_get_filter_argument_values_single(self):
        self._get_filter_argument_values_test('f1 v1 c1', ['f1'])

    def test_get_filter_argument_values_multiple(self):
        self._get_filter_argument_values_test('f1 f2 v1 c1 c2', ['f1', 'f2'])
    
    def _get_command_argument_values_test(self, input, output):
        self._get_argument_value_test(input, output, \
            commandfactory.ParsedCommand.get_command_argument_values)
    
    def _get_filter_argument_values_test(self, input, output):
        self._get_argument_value_test(input, output, \
            commandfactory.ParsedCommand.get_filter_argument_values)
    
    def _get_get_verb_value_test(self, input, output):
        self._get_argument_value_test(input, output, \
            commandfactory.ParsedCommand.get_verb_value)
    
    def _get_argument_value_test(self, input, output, method):
        command = self._create_command(input)
        args = method(command)
        self.assertEqual(output, args)

    def _create_command(self, args_string):
        '''
        Creates a command with arguments decoded from args_string.
        Arguments are separated by spaces.
        Arguments beginning with 'c' will be added as command arguments.
        Arguments beginning with 'f' will be added as filters.
        Arguments beginning with 'v' will be added as verbs.
        '''
        command = commandfactory.ParsedCommand()
        arg_index = 1
        for arg_string in args_string.split():
            if arg_string[0] == 'c':
                arg_type = commandfactory.ArgumentType.command_argument
            elif arg_string[0] == 'f':
                arg_type = commandfactory.ArgumentType.filter
            elif arg_string[0] == 'v':
                arg_type = commandfactory.ArgumentType.verb
            else:
                raise Exception(f'Unknown test argument type: [{arg_string[0]}]')
            arg = commandfactory.ParsedArgument(arg_index, arg_string, arg_type)
            command.arguments.append(arg)
            arg_index += 1
        return command

class ParsedArgumentTests(unittest.TestCase):
    def test_str(self):
        arg = commandfactory.ParsedArgument(1, 'test 1', 'arg type')
        self.assertEqual('1 arg type: test 1', str(arg))



    '''
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
    '''