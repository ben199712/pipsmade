#!/bin/bash

# Django-only startup script (no gunicorn)
PORT=${PORT:-8000}

echo "=== Starting Django Development Server ==="
echo "PORT: $PORT"
echo "Time: $(date)"

# Setup environment
echo "Setting up environment..."

# Check database
if [ ! -f "db.sqlite3" ]; then
    echo "Creating database..."
    python manage.py migrate
fi

# Always collect static files to ensure they're up to date
echo "Collecting static files..."
python manage.py collectstatic --no-input --clear

# Verify static files were collected
if [ -d "staticfiles" ]; then
    echo "Static files collected successfully"
    echo "Static files count: $(find staticfiles -type f | wc -l)"
    echo "Static files directory contents:"
    ls -la staticfiles/
else
    echo "ERROR: Static files directory not found after collection!"
    exit 1
fi

# Test Django configuration
echo "Testing Django configuration..."
python manage.py check
if [ $? -ne 0 ]; then
    echo "Django configuration check failed!"
    exit 1
fi

echo "Starting Django development server on port $PORT..."
echo "This server is more reliable than gunicorn for debugging"
echo "Static files should be available at /static/"

# Start Django development server
exec python manage.py runserver 0.0.0.0:$PORT 