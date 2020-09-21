'''
A module providing task commands.
'''

import commands.commandbase as commandbase
import commandline
import filters.allbatchfilter as allbatchfilter
import typefactory


class CommandFactory(typefactory.TypeFactory):
    def __init__(self, command_context):
        super().__init__(commandbase.CommandParserBase)
        self._command_context = command_context

    def get_command(self, args):
        if not args:
            args = self._command_context.settings.command_default.split()

        if not args:
            exit_code = commandline.ExitCodes.no_command_specified_error
            raise commandline.ExitCodeException(exit_code=exit_code)

        parsed_arguments = self._parse(args)
        if self._command_context.settings.debug_command_parser:
            for parsed_argument in parsed_arguments:
                print(parsed_argument)
        
        verb_arguments = [a for a in parsed_arguments if a.arg_type == 'verb']
        if len(verb_arguments) == 0:
            exit_code = commandline.ExitCodes.unknown_command_error
            raise commandline.ExitCodeException(exit_code=exit_code)
        verb_argument = verb_arguments[0]

        # TODO: if filters return 1 task use info command

        # TODO: if filters return multiple tasks use list command

        parsers = [p for p in self.types if p.command_name == verb_argument.text]
        if parsers == None:
            raise Exception('Parser not found for verb: [{}]'.format(verb_argument))
        parser = parsers[0]

        command_arguments = [a.text for a in parsed_arguments if a.arg_type == 'argument']
        command = parser.parse(self._command_context, command_arguments)

        batch_filter = allbatchfilter.AllBatchFilter()
        filter_arguments = [a for a in parsed_arguments if a.arg_type == 'filter']
        for filter_arguments in filter_arguments:
            batch_filter.add_filter(self._command_context.filter_factory.parse(args[0]))
        confirm_filter = parser.get_confirm_filter(self._command_context)
        if confirm_filter:
            batch_filter.add_filter(confirm_filter)
        command.filter = batch_filter
        
        return command
    
    def _parse(self, args):
        verb_index = self._find_verb_index(args)
        parsed_arguments = []
        for arg_index in range(0, len(args)):
            if arg_index == verb_index:
                arg_type = 'verb'
            elif arg_index < verb_index:
                arg_type = 'filter'
            else:
                arg_type = 'argument'
            parsed_argument = ParsedArgument(arg_index, args[arg_index], arg_type)
            parsed_arguments.append(parsed_argument)
            if self._command_context.settings.debug_command_parser == True:
                print(parsed_argument)
        return parsed_arguments
    
    def _find_verb_index(self, args):
        for arg_index in range(0, len(args)):
            for parser in self.types:
                if parser.command_name == args[arg_index]:
                    return arg_index
        return -1


class ParsedArgument:
    def __init__(self, arg_index, text, arg_type):
        self.arg_index = arg_index
        self.text = text
        self.arg_type = arg_type

    def __str__(self):
        return '{:2} {:8}: {}'.format(self.arg_index, self.arg_type, self.text)
