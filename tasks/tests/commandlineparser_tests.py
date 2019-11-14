import unittest

import commandlineparser as cli


class CommandLineParserTests(unittest.TestCase):
    def test_name_collects_multiple_args(self):
        args = []
        args.append('arg1')
        args.append('arg2')
        args.append('arg3')
        result = cli.CommandLineParser().parse(args)
        result.name = 'arg1 arg2 arg3'

