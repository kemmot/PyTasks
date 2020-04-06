#! /bin/bash

dir=$(dirname "${0}")
dir=$(realpath "$dir/../tasks")
pushd "$dir"

markdown2 ../README.md --extras tables,header-ids,fenced-code-blocks > ../README.html

popd
