#!/usr/bin/env bash
# exit on error
set -o errexit

# Upgrade pip first
pip install --upgrade pip

# Install packages with better error handling
pip install -r requirements.txt --no-cache-dir

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate 