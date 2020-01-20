pushd %~dp0..\tasks
python -m unittest discover tests -p "*_test.py" -v
REM coverage run -m unittest discover tests -p "*_test.py"
REM coverage report -m --omit="*_test.py"
popd
