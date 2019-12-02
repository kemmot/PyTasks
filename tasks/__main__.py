#!/usr/bin/env python3

'''
The main module for the tasks program.
'''

import logging
import os
import sys

import commands
import commandlineparser as cli
import storage


FORMAT = '%(message)s'
logging.basicConfig(format=FORMAT, level='INFO')

FILENAME = os.path.join(os.path.split(os.path.dirname(os.path.abspath(__file__)))[0], 'todo.txt')
ARGS = cli.CommandLineParser().parse(sys.argv[1:])
STORAGE = storage.TaskWarriorPendingStorage(FILENAME)
COMMAND_FACTORY = commands.CommandFactory(STORAGE)
COMMAND = COMMAND_FACTORY.get_command(ARGS)
COMMAND.execute()
