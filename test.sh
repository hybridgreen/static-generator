export PYTHONPATH="$PYTHONPATH:$(pwd)/src"

python3 -m unittest discover -s src/tests -v