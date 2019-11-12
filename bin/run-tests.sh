pushd ../tasks
python3 -m unittest discover tests -p "_tests.py" -v
coverage run -m unittest discover tests -p "*_tests.py"
coverage report -m --omit="*_tests.py"
popd
