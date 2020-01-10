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
                help='The available commands.')

        add_parser = subparsers.add_parser('add', help='Adds a task.')
        add_parser.add_argument('name', nargs='+', help='The name of the new item.')

        add_parser = subparsers.add_parser('done', help='Marks a task as complete.')
        add_parser.add_argument('filter', type=int, help='The task filter.')

        subparsers.add_parser('list', help='List existing tasks.')

        return parser.parse_args(args)
