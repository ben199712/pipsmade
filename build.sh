#!/usr/bin/env bash
# exit on error
set -o errexit

# Upgrade pip first
pip install --upgrade pip

# Install packages with optimizations for free plan
pip install -r requirements.txt --no-cache-dir --prefer-binary

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate 