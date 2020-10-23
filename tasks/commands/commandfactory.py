'''
A module providing task commands.
'''

import logging

import commands.commandbase as commandbase
import commandline
import filters.allbatchfilter as allbatchfilter
import typefactory


class CommandFactory(typefactory.TypeFactory):
    def __init__(self, command_context):
        super().__init__(commandbase.CommandParserBase)
        self._command_context = command_context
        self._logger = logging.getLogger(__class__.__name__)

    def get_command(self, args):
        if not args:
            args = self._command_context.settings.command_default.split()

        if not args:
            exit_code = commandline.ExitCodes.no_command_specified_error
            raise commandline.ExitCodeException(exit_code=exit_code)

        command_names = [a.command_name for a in self.types]
        parsed_command = CommandParser(command_names).parse(args)
        for parsed_argument in parsed_command.arguments:
            self._logger.debug(parsed_argument)
        
        verb_argument = parsed_command.get_verb()

        # TODO: if filters return 1 task use info command

        # TODO: if filters return multiple tasks use list command

        parsers = [p for p in self.types if p.command_name == verb_argument.text]
        if parsers == None:
            raise Exception('Parser not found for verb: [{}]'.format(verb_argument))
        parser = parsers[0]

        command_arguments = parsed_command.get_command_argument_values()
        command = parser.parse(self._command_context, command_arguments)

        batch_filter = allbatchfilter.AllBatchFilter()
        filter_arguments = parsed_command.get_filter_argument_values()
        for filter_arguments in filter_arguments:
            batch_filter.add_filter(self._command_context.filter_factory.parse(args[0]))
        confirm_filter = parser.get_confirm_filter(self._command_context)
        if confirm_filter:
            batch_filter.add_filter(confirm_filter)
        command.filter = batch_filter
        
        return command
    

class CommandParser:
    def __init__(self, command_names):
        self._command_names = command_names
        self._logger = logging.getLogger(__class__.__name__)
    
    def parse(self, args):
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
            self._logger.debug(parsed_argument)
        return parsed_command
    
    def _find_verb_index(self, args):
        for arg_index in range(0, len(args)):
            for command_name in self._command_names:
                if command_name == args[arg_index]:
                    return arg_index
        return -1


class ParsedCommand:
    def __init__(self):
        self._arguments = []
    
    @property
    def arguments(self):
        return self._arguments
    
    def get_verb(self):
        verb_arguments = self._get_arguments_by_type(ArgumentType.verb)
        if len(verb_arguments) == 0:
            exit_code = commandline.ExitCodes.unknown_command_error
            raise commandline.ExitCodeException(exit_code=exit_code)
        return verb_arguments[0]
    
    def get_command_argument_values(self):
        return self._get_argument_values_by_type(ArgumentType.command_argument)
    
    def get_filter_argument_values(self):
        return self._get_argument_values_by_type(ArgumentType.filter)
    
    def _get_argument_values_by_type(self, argument_type):
        return [a.text for a in self._get_arguments_by_type(argument_type)]
    
    def _get_arguments_by_type(self, argument_type):
        return [a for a in self.arguments if a.arg_type == argument_type]


class ParsedArgument:
    def __init__(self, arg_index, text, arg_type):
        self.arg_index = arg_index
        self.text = text
        self.arg_type = arg_type

    def __str__(self):
        return '{} {}: {}'.format(self.arg_index, self.arg_type, self.text)


class ArgumentType:
    command_argument = 'argument'
    filter = 'filter'
    verb = 'verb'
