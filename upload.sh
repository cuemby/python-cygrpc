#!/usr/bin/env bash
rm -rf build
rm -rf dist
rm -rf cygrpc.egg-info

python setup.py sdist bdist_wheel
python -m twine check dist/*
python -m twine upload dist/*