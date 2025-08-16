#!/bin/bash

# Simple startup script
PORT=${PORT:-8000}

echo "Starting Django on port $PORT"

# Run migrations if needed
python manage.py migrate

# Start Django development server (more reliable than gunicorn for debugging)
python manage.py runserver 0.0.0.0:$PORT 