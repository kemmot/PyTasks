#!/bin/bash

BINPATH=`dirname $0`
pushd "$BINPATH/../tasks/"
pylint * \
	--disable=missing-docstring \
	--disable=no-self-use \
	--disable=too-few-public-methods \
	--ignore=tests,tasks.ini,tasks.log,tasks.logging.yaml,input.txt
popd
