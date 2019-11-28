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

command_factory = commands.CommandFactory(FILENAME)
command = command_factory.get_command(args)
command.execute()
