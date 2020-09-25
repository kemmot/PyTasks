@echo off
pushd %~dp0..\tasks
pylint "..\tasks" --disable=missing-docstring --disable=no-self-use --disable=too-few-public-methods
popd
