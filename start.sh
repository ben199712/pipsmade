#!/bin/bash

# Set default port if not provided
PORT=${PORT:-8000}

# Start gunicorn with the port
exec gunicorn pipsmade.wsgi:application --bind 0.0.0.0:$PORT 