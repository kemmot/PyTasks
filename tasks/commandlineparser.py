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
        subparsers = parser.add_subparsers( \
                dest='command', \
                help='available commands')

        add_parser = subparsers.add_parser('add', help='adds a task')
        add_parser.add_argument('name', nargs='+', help='the item name')
        
        add_parser = subparsers.add_parser('done', help='marks a task as complete')
        add_parser.add_argument('filter', type=int, help='the task filter')

        subparsers.add_parser('list', help='list tasks')

        return parser.parse_args(args)
