@echo off
echo "%~dp0"
pylint "%~dp0\..\tasks" --disable=missing-docstring --disable=no-self-use --disable=too-few-public-methods
