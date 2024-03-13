#!/bin/bash

echo "Running pyup_dirs..."
pyup_dirs --py38-plus --recursive src tests

echo "Running ruff..."
ruff src tests --fix

echo "Running black..."
black src tests
