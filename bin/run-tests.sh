#!/bin/bash

dir=$(dirname "${0}")
dir=$(realpath "$dir/../tasks")
pushd "$dir"

python3 -m unittest discover tests -p "*_test.py" -v
exit_code=$?

if [ $exit_code -eq 0 ]
then
	coverage run -m unittest discover tests -p "*_test.py"
	coverage report -m --omit="*_test.py"
	exit_code=$?
fi

popd
exit $exit_code
