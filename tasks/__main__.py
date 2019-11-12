#!/usr/bin/env python3

import sys

import commandlineparser as cli

args = cli.CommandLineParser().parse(sys.argv)
print('add item: {}'.format(' '.join(args.name)))
