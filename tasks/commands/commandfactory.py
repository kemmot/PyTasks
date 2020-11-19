'''
A module providing task commands.
'''

import logging
import sys

import commands.commandbase as commandbase
import commands.multicommand as multicommand
import commandline
import filters.allbatchfilter as allbatchfilter
import typefactory


class CommandFactory(typefactory.TypeFactory):
    def __init__(self, parser, command_context):
        super().__init__(commandbase.CommandParserBase)
        self._parser = parser
        self._command_context = command_context
        self._logger = logging.getLogger(__class__.__name__)

    def get_command(self, args):
        if not args:
            args = self._command_context.settings.command_default.split()

        command_names = [a.command_name for a in self.types]
        for command_name in command_names:
            self._parser.add_command_name(command_name)
        parsed_command = self._parser.parse(args)
        self._logger.debug(parsed_command)

        batch_filter = self._get_filters(parsed_command)
        verb_argument = parsed_command.get_verb_value()
        if verb_argument:
            command_arguments = parsed_command.get_command_argument_values()
            parser,command = self._get_command(verb_argument, command_arguments)
            if parser:
                confirm_filter = parser.get_confirm_filter(self._command_context)
                if confirm_filter:
                    batch_filter.add_filter(confirm_filter)
        else:
            zero_item_command = self._get_command(self._command_context.settings.command_default_zero_items)[1]
            one_item_command = self._get_command(self._command_context.settings.command_default_one_item)[1]
            multi_item_command = self._get_command(self._command_context.settings.command_default_multi_items)[1]
            command = multicommand.MultiCommand(self._command_context, zero_item_command, one_item_command, multi_item_command)

        command.filter = batch_filter
        return command
    
    def _get_command(self, verb, command_arguments=[]):
        parsers = [p for p in self.types if p.command_name == verb]
        if not parsers:
            raise Exception('Parser not found for verb: [{}]'.format(verb))
        parser = parsers[0]
        command = parser.parse(self._command_context, command_arguments)
        return parser,command

    def _get_filters(self, parsed_command):
        batch_filter = allbatchfilter.AllBatchFilter()
        filter_arguments = parsed_command.get_filter_argument_values()
        for filter_argument in filter_arguments:
            batch_filter.add_filter(self._command_context.filter_factory.parse(filter_argument))
        return batch_filter


class CommandParser:
    def __init__(self):
        self._command_names = []
        self._logger = logging.getLogger(__class__.__name__)

    def add_command_name(self, name):
        self._command_names.append(name)

    def parse(self, args):
        if args is None:
            raise Exception('args cannot be None')
        verb_index = self._find_verb_index(args)
        parsed_command = ParsedCommand()
        for arg_index in range(0, len(args)):
            if arg_index == verb_index:
                arg_type = ArgumentType.verb
            elif arg_index < verb_index:
                arg_type = ArgumentType.filter
            else:
                arg_type = ArgumentType.command_argument
            parsed_argument = ParsedArgument(arg_index, args[arg_index], arg_type)
            parsed_command.arguments.append(parsed_argument)
        return parsed_command

    def _find_verb_index(self, args):
        arg_index = 0
        for arg in args:
            for command_name in self._command_names:
                if command_name == arg:
                    return arg_index
            arg_index += 1
        return sys.maxsize


class ParsedCommand:
    def __init__(self):
        self._arguments = []

    @property
    def arguments(self):
        return self._arguments

    def get_verb_value(self):
        verb_arguments = self._get_argument_values_by_type(ArgumentType.verb)
        if not verb_arguments:
            return ''
        return verb_arguments[0]

    def get_command_argument_values(self):
        return self._get_argument_values_by_type(ArgumentType.command_argument)

    def get_filter_argument_values(self):
        return self._get_argument_values_by_type(ArgumentType.filter)

    def _get_argument_values_by_type(self, argument_type):
        return [a.text for a in self._get_arguments_by_type(argument_type)]

    def _get_arguments_by_type(self, argument_type):
        return [a for a in self.arguments if a.arg_type == argument_type]

    def __str__(self):
        description = ''
        for arg in self.arguments:
            description += f'[{arg}]'
        return description


class ParsedArgument:
    def __init__(self, arg_index, text, arg_type):
        self.arg_index = arg_index
        self.text = text
        self.arg_type = arg_type

    def __str__(self):
        return 'Argument: {}, type: {}, value: {}'.format(self.arg_index, self.arg_type, self.text)


class ArgumentType:
    command_argument = 'command argument'
    filter = 'filter'
    verb = 'verb'
