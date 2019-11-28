#!/bin/bash

BINPATH=`dirname $0`
pylint "$BINPATH/../tasks"
