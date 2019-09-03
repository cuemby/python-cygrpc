#!/usr/bin/env bash
rm -rf .eggs
rm -rf build
rm -rf dist
rm -rf cygrpc.egg-info
rm -rf cygrpc.py.egg-info

python3 -m twine check dist/*
#python3 -m twine upload dist/*