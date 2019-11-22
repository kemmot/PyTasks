pushd %~dp0..\tasks
python -m unittest discover tests -p "_tests.py" -v
rem coverage run -m unittest discover tests -p "*_tests.py"
rem coverage report -m --omit="*_tests.py"
popd