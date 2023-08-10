#!/usr/bin/env bash
python setup.py sdist bdist_wheel && twine upload ./dist/*

pip install ./dist/*.whl -U
rm -rf ./build ./dist ./*.egg* ./.eggs
exit
