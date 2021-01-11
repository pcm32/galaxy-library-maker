rm -rf venv-test
python -m venv venv-test
source venv-test/bin/activate
pip install --upgrade pip
pip install wheel
pip install . ephemeris galaxy-parsec
