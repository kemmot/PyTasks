#!/usr/bin/env python3

import sys

import commandlineparser as cli
import commands as commands


filename = '~/tasks.txt'

args = cli.CommandLineParser().parse(sys.argv[1:])
command = commands.AddTaskCommand()
command.filename = filename
command.name = args.name
command.execute()
