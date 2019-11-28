#!/usr/bin/env python3

'''
The main module for the tasks program.
'''

import logging
import os
import sys

import commands
import commandlineparser as cli


FORMAT = '%(message)s'
logging.basicConfig(format=FORMAT, level='INFO')

FILENAME = os.path.expanduser('~/tasks.txt')

args = cli.CommandLineParser().parse(sys.argv[1:])

if args.command == 'add':
    command = commands.AddTaskCommand()
    command.filename = FILENAME
    command.name = ' '.join(args.name)
    command.execute()
else:
    print('no command found')
