#!/usr/bin/env python3

'''
The main module for the tasks program.
'''

import logging
import os
import sys

import commands
import commandlineparser as cli
import formatters
import entities


FORMAT = '%(message)s'
logging.basicConfig(format=FORMAT, level='INFO')

FILENAME = os.path.expanduser('~/tasks.txt')

args = cli.CommandLineParser().parse(sys.argv[1:])

if args.command == 'add':
    task = entities.Task()
    task.name = ' '.join(args.name)
    
    formatter = formatters.TaskWarriorFormatter()

    command = commands.AddTaskCommand(formatter)
    command.filename = FILENAME
    command.task = task
    command.execute()
else:
    print('no command found')
