export PYTHONPATH="$PYTHONPATH:$(pwd)/src"

python3 -m unittest discover -s src/tests -v > test_result.txt -c 2>&1
