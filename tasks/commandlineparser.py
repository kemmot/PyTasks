import argparse
import sys


class CommandLineParser:
    def parse(self, args):
        parser = argparse.ArgumentParser(prog='tasks')
        parser.add_argument('name', nargs='+', help='the item name')
        return parser.parse_args(args)

