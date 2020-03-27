pushd %~dp0..\tasks
python -m unittest discover tests -p "*_test.py" -v
coverage run -m unittest discover tests -p "*_test.py"
coverage report -m --omit="*_test.py"
popd
