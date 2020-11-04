export PYTHONPATH=$(pwd)/backend;  
pytest -v backend/src/tests;

if [ $? -eq "1" ]; then
	exit 1;
fi
