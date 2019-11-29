import unittest

import commandlineparser as cli


class CommandLineParserTests(unittest.TestCase):        
    def test_no_args_parses_no_command(self):
        args = []
        result = cli.CommandLineParser().parse(args)
        self.assertEqual(result.command, None)

    def test_add_command_parses(self):
        args = []
        args.append('add')
        args.append('arg2')
        result = cli.CommandLineParser().parse(args)
        self.assertEqual(result.command, 'add')
        self.assertEqual(result.name, ['arg2'])

    def test_add_command_collects_multiple_name_args(self):
        args = []
        args.append('add')
        args.append('arg2')
        args.append('arg3')
        result = cli.CommandLineParser().parse(args)
        self.assertEqual(result.name, ['arg2', 'arg3'])
        
    def test_list_command_parses(self):
        args = []
        args.append('list')
        result = cli.CommandLineParser().parse(args)
        self.assertEqual(result.command, 'list')
        
