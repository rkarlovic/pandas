#!/bin/bash

# Navigate to the directory containing the requirements.txt file
cd "$(dirname "$0")"

# Create a virtual environment named 'venv'
python -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install the packages listed in requirements.txt
pip install -r requirements.txt
