pushd ../tasks
python3 -m unittest discover tests -p "*_test.py" -v
if [ $? -eq 0 ]
then
	coverage run -m unittest discover tests -p "*_test.py"
	coverage report -m --omit="*_test.py"
fi
popd
