#!/usr/bin/env python3

import sys

import commandlineparser as cli

args = cli.CommandLineParser().parse(sys.argv[1:])
print('add item: {}'.format(' '.join(args.name)))
