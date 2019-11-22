#!/usr/bin/env python3

'''
The main module for the tasks program.
'''

import sys

import commandlineparser as cli
import commands as commands


FILENAME = '~/tasks.txt'

args = cli.CommandLineParser().parse(sys.argv[1:])

command = commands.AddTaskCommand()
command.filename = FILENAME
command.name = args.name
command.execute()
