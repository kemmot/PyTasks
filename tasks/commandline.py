'''
Module used for parsing command line arguments.
'''

import argparse


class ExitCodes:
    success = 0
    unknown_error = 99

    @staticmethod
    def get_description(value):
        if value == ExitCodes.success:
            description = 'Success'
        else:
            description = 'Unknown Error'
        return description


class ExitCodeException(Exception):
    def __init__(self, message, exit_code=ExitCodes.unknown_error):
        Exception.__init__(self, message)
        self._exit_code = exit_code

    @property
    def exit_code(self):
        return self._exit_code


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
