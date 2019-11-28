pushd ../tasks
python3 -m unittest discover tests -p "*_tests.py" -v
if [ $? -eq 0 ]
then
	coverage run -m unittest discover tests -p "*_tests.py"
	coverage report -m --omit="*_tests.py"
fi
popd
