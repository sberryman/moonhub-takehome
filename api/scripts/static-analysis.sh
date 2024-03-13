#!/bin/bash
set -e

echo "Running mypy..."
mypy src

echo "Running bandit..."
bandit -c pyproject.toml -r api
