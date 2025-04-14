#!/bin/bash

VENV_DIR="$(dirname "$0")/venv"
REQUIREMENTS_FILE="$(dirname "$0")/requirements.txt"

if [ ! -d "$VENV_DIR" ]; then
  echo "Creating virtual environment..."
  python3 -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"
if [ -f "$REQUIREMENTS_FILE" ]; then
  echo "Installing dependencies from requirements.txt..."
  pip install -r "$REQUIREMENTS_FILE"
else
  echo "No requirements.txt found, skipping install."
fi

echo "Running browser.py..."
python3 "$(dirname "$0")/browser.py"
