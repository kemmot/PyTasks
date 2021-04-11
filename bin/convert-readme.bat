pushd %~dp0..\tasks
python -m markdown2 ../README.md --extras tables,header-ids,fenced-code-blocks > ..\README.html
popd
