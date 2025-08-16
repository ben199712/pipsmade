#!/bin/bash

# Set default port if not provided
PORT=${PORT:-8000}

# Debug information
echo "Starting Django application..."
echo "PORT: $PORT"
echo "DJANGO_SETTINGS_MODULE: $DJANGO_SETTINGS_MODULE"
echo "Current directory: $(pwd)"
echo "Files in current directory: $(ls -la)"

# Check if database exists
if [ -f "db.sqlite3" ]; then
    echo "Database file exists"
else
    echo "Database file not found, creating..."
    python manage.py migrate
fi

# Check if static files exist
if [ -d "staticfiles" ]; then
    echo "Static files directory exists"
    echo "Static files count: $(find staticfiles -type f | wc -l)"
else
    echo "Static files directory not found"
fi

# Start gunicorn with the port and better error handling
echo "Starting gunicorn on port $PORT..."
exec gunicorn pipsmade.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 2 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info 