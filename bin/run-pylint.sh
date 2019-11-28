#!/bin/bash

BINPATH=`dirname $0`
pushd "$BINPATH/../tasks"
pylint * \
	--disable=missing-docstring \
	--disable=no-self-use \
	--disable=too-few-public-methods
popd
