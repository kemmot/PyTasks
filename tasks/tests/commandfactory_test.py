import unittest
from unittest import mock

import commands.commandfactory as commandfactory
import commandline
import filters.allbatchfilter as allbatchfilter


class CommandFactoryTests(unittest.TestCase):
    def setUp(self):
        self.command_name = 'test'
        self.mock_command = mock.Mock()
        self.mock_filter = mock.Mock()

        self.mock_command_type = mock.Mock()
        self.mock_command_type.command_name = self.command_name
        self.mock_command_type.parse = mock.MagicMock(return_value=self.mock_command)
        
        self.mock_context = mock.Mock()
        self.mock_context.filter_factory = mock.Mock()
        self.mock_context.filter_factory.parse = mock.MagicMock(return_value=self.mock_filter) 
        self.mock_context.settings = mock.Mock()

        self.mock_parser = mock.Mock()
        self.mock_parser.add_command_name = mock.Mock()

        self.factory = commandfactory.CommandFactory(self.mock_parser, self.mock_context)
        self.factory.register_type(self.mock_command_type)

    def test_constructor_success(self):
        commandfactory.CommandFactory(mock.Mock(), mock.Mock())

    def test_get_command_empty_args_no_default(self):
        context = mock.Mock()
        context.settings = mock.Mock()
        context.settings.command_default = ''
        factory = commandfactory.CommandFactory(mock.Mock(), context)
        with self.assertRaises(Exception):
            factory.get_command(None)

    def test_get_command_none_args(self):
        args = None
        filter_args = ['f1']
        command_args = ['c1', 'c2']
        default_args = 'test1 test2 test3'
        self.get_command_test(args, filter_args, command_args, default_args)

    def test_get_command_empty_args(self):
        args = []
        filter_args = ['f1']
        command_args = ['c1', 'c2']
        default_args = 'test1 test2 test3'
        self.get_command_test(args, filter_args, command_args, default_args)

    def test_get_command(self):
        args = ['f1', 'v1', 'c1', 'c2']
        filter_args = ['f1']
        command_args = ['c1', 'c2']
        default_args = 'test1 test2 test3'
        self.get_command_test(args, filter_args, command_args, default_args)

    def test_get_command_no_matching_commands(self):
        args = ['f1', 'v1', 'c1', 'c2']
        filter_args = ['f1']
        command_args = ['c1', 'c2']
        default_args = 'test1 test2 test3'
        self.command_name = 'unknown'
        with self.assertRaises(Exception):
            self.get_command_test(args, filter_args, command_args, default_args)

    def get_command_test(self, args, filter_args, command_args, default_args):       
        self.mock_context.settings.command_default = default_args
        parsed_command = self.create_parsed_command(filter_args, command_args)
        self.mock_parser.parse = mock.MagicMock(return_value=parsed_command)
        
        result = self.factory.get_command(args)

        self.assertEqual(self.mock_command, result)
        self.assertIsInstance(self.mock_command.filter, allbatchfilter.AllBatchFilter)

        self.mock_parser.add_command_name.assert_called_once_with(self.command_name)
        if args:
            expected_args = args
        else:
            expected_args = self.mock_context.settings.command_default.split()
        self.mock_parser.parse.assert_called_once_with(expected_args)
        self.mock_command_type.parse.assert_called_once_with(self.mock_context, command_args)
        self.mock_context.filter_factory.parse.assert_called_once_with(filter_args[0])

    def create_parsed_command(self, filter_args, command_args):
        parsed_command = mock.Mock()
        parsed_command.get_verb_value = mock.MagicMock(return_value=self.command_name)
        parsed_command.get_command_argument_values = mock.MagicMock(return_value=command_args)
        parsed_command.get_filter_argument_values = mock.MagicMock(return_value=filter_args)
        return parsed_command

class CommandParserTests(unittest.TestCase):
    
    def test_parse_none_args_raises(self):
        parser = commandfactory.CommandParser()
        with self.assertRaises(Exception):
            parser.parse(None)
    
    def test_parse_empty_args(self):
        self._test_parse(['v1'], [])
    
    def test_parse_only_verb(self):
        self._test_parse(['v1'], ['v1'])
    
    def test_parse_filter_verb(self):
        self._test_parse(['v1'], ['f1', 'v1'])
    
    def test_parse_verb_cmd(self):
        self._test_parse(['v1'], ['v1', 'c1'])
    
    def test_parse_filter_verb_cmd(self):
        self._test_parse(['v1'], ['f1', 'v1', 'c1'])
    
    def _test_parse(self, verbs, input):
        parser = commandfactory.CommandParser()
        for verb in verbs:
            parser.add_command_name(verb)
        command = parser.parse(input)
        self.assertIsNotNone(command)
        self.assertEqual(len(input), len(command.arguments))
        arg_index = 0
        for arg_string in input:
            arg = command.arguments[arg_index]
            arg_type = ArgumentTypeDecoder.decode(arg_string)
            self._assert_argument(arg, arg_index, arg_type, arg_string)
            arg_index += 1
    
    def _assert_argument(self, arg, arg_index, arg_type, text):
        self.assertEqual(arg_index, arg.arg_index)
        self.assertEqual(arg_type, arg.arg_type)
        self.assertEqual(text, arg.text)


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
    
    def test_str(self):
        command = commandfactory.ParsedCommand()
        command.arguments.append('f1')
        command.arguments.append('v1')
        command.arguments.append('c1')
        result = str(command)
        self.assertEqual('[f1][v1][c1]', result)
    
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
        command = commandfactory.ParsedCommand()
        arg_index = 1
        for arg_string in args_string.split():
            arg_type = ArgumentTypeDecoder.decode(arg_string)
            arg = commandfactory.ParsedArgument(arg_index, arg_string, arg_type)
            command.arguments.append(arg)
            arg_index += 1
        return command


class ArgumentTypeDecoder:
    @staticmethod
    def decode(arg_string):
        '''
        Creates a command with arguments decoded from args_string.
        Arguments are separated by spaces.
        Arguments beginning with 'c' will be added as command arguments.
        Arguments beginning with 'f' will be added as filters.
        Arguments beginning with 'v' will be added as verbs.
        '''
        if arg_string[0] == 'c':
            arg_type = commandfactory.ArgumentType.command_argument
        elif arg_string[0] == 'f':
            arg_type = commandfactory.ArgumentType.filter
        elif arg_string[0] == 'v':
            arg_type = commandfactory.ArgumentType.verb
        else:
            raise Exception(f'Unknown test argument type: [{arg_string[0]}]')
        return arg_type


class ParsedArgumentTests(unittest.TestCase):
    def test_str(self):
        arg = commandfactory.ParsedArgument(1, 'test 1', 'arg type')
        self.assertEqual('1 arg type: test 1', str(arg))
