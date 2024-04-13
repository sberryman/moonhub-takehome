#!/bin/bash

echo "Running pyup_dirs..."
pyup_dirs --py38-plus --recursive src tests scripts

echo "Running ruff..."
ruff src tests scripts --fix

echo "Running black..."
black src tests scripts
