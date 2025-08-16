#!/bin/bash

# Robust startup script with crash prevention
PORT=${PORT:-8000}

echo "=== Starting Robust Django Application ==="
echo "PORT: $PORT"
echo "Time: $(date)"

# Function to check if Django is responding
check_django_health() {
    echo "Checking Django health..."
    # Wait a bit for Django to start
    sleep 5
    
    # Try to make a simple request
    if command -v curl >/dev/null 2>&1; then
        response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:$PORT/ || echo "000")
        if [ "$response" = "200" ] || [ "$response" = "404" ] || [ "$response" = "302" ]; then
            echo "Django is responding (HTTP $response)"
            return 0
        else
            echo "Django is not responding properly (HTTP $response)"
            return 1
        fi
    else
        echo "curl not available, skipping health check"
        return 0
    fi
}

# Function to restart Django if it crashes
restart_django() {
    echo "Restarting Django..."
    pkill -f gunicorn || true
    sleep 2
    start_django
}

# Function to start Django
start_django() {
    echo "Starting Django with gunicorn..."
    
    # Start gunicorn in background
    gunicorn pipsmade.wsgi:application \
        --bind 0.0.0.0:$PORT \
        --workers 1 \
        --timeout 300 \
        --keep-alive 5 \
        --max-requests 1000 \
        --max-requests-jitter 100 \
        --access-logfile - \
        --error-logfile - \
        --log-level debug \
        --preload \
        --daemon
    
    # Wait for startup
    sleep 3
    
    # Check health
    if check_django_health; then
        echo "Django started successfully!"
        # Keep script running and monitor
        while true; do
            sleep 30
            if ! check_django_health; then
                echo "Django crashed, restarting..."
                restart_django
            fi
        done
    else
        echo "Django failed to start properly"
        exit 1
    fi
}

# Main startup process
echo "Setting up environment..."

# Check database
if [ ! -f "db.sqlite3" ]; then
    echo "Creating database..."
    python manage.py migrate
fi

# Check static files
if [ ! -d "staticfiles" ]; then
    echo "Collecting static files..."
    python manage.py collectstatic --no-input
fi

# Test Django configuration
echo "Testing Django configuration..."
python manage.py check
if [ $? -ne 0 ]; then
    echo "Django configuration check failed!"
    exit 1
fi

# Start Django
start_django 