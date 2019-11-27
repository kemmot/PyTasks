#!/usr/bin/env python3

'''
The main module for the tasks program.
'''

import os
import sys

import commands
import commandlineparser as cli


FILENAME = os.path.expanduser('~/tasks.txt')

args = cli.CommandLineParser().parse(sys.argv[1:])

command = commands.AddTaskCommand()
command.filename = FILENAME
command.name = ' '.join(args.name)
command.execute()
