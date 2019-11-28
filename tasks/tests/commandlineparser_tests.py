import unittest

import commandlineparser as cli


class CommandLineParserTests(unittest.TestCase):
    def test_name_collects_multiple_args(self):
        args = []
        args.append('add')
        args.append('arg2')
        args.append('arg3')
        result = cli.CommandLineParser().parse(args)
        self.assertEqual(result.command, 'add')
        self.assertEqual(result.name, ['arg2', 'arg3'])
