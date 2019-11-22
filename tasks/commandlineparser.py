'''
Module used for parsing command line arguments.
'''

import argparse


class CommandLineParser:
    '''
    A command line argument parser implemented using the argparse library.
    '''
    def parse(self, args):
        '''
        Parses the arguments.
        '''
        parser = argparse.ArgumentParser(prog='tasks')
        parser.add_argument('name', nargs='+', help='the item name')
        return parser.parse_args(args)
