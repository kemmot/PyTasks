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
ARGS = cli.CommandLineParser().parse(sys.argv[1:])
COMMAND_FACTORY = commands.CommandFactory(FILENAME)
COMMAND = COMMAND_FACTORY.get_command(ARGS)
COMMAND.execute()
