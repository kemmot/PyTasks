#!/bin/bash

BINPATH=`dirname $0`
pushd "$BINPATH/../tasks"
pylint .
popd
