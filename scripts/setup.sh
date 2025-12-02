#!/bin/bash
set -e

echo "Setting up environment..."
python -m pip install --upgrade pip
pip install -r requirements.txt

echo "Setup complete."
