#!/bin/bash

# Set default port if not provided
PORT=${PORT:-8000}

# Debug information
echo "Starting Django application..."
echo "PORT: $PORT"
echo "DJANGO_SETTINGS_MODULE: $DJANGO_SETTINGS_MODULE"
echo "Current directory: $(pwd)"
echo "Files in current directory: $(ls -la)"

# Check if database exists and is accessible
if [ -f "db.sqlite3" ]; then
    echo "Database file exists"
    # Test database connection
    python manage.py check --database default
    if [ $? -eq 0 ]; then
        echo "Database connection successful"
    else
        echo "Database connection failed, recreating..."
        rm -f db.sqlite3
        python manage.py migrate
    fi
else
    echo "Database file not found, creating..."
    python manage.py migrate
fi

# Check if static files exist
if [ -d "staticfiles" ]; then
    echo "Static files directory exists"
    echo "Static files count: $(find staticfiles -type f | wc -l)"
else
    echo "Static files directory not found, collecting..."
    python manage.py collectstatic --no-input
fi

# Health check - test Django startup
echo "Testing Django startup..."
python manage.py check
if [ $? -ne 0 ]; then
    echo "Django check failed, exiting..."
    exit 1
fi

# Start gunicorn with the port and better error handling
echo "Starting gunicorn on port $PORT..."
exec gunicorn pipsmade.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 1 \
    --timeout 300 \
    --keep-alive 5 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --access-logfile - \
    --error-logfile - \
    --log-level debug \
    --preload 