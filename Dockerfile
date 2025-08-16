FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=pipsmade.settings_production

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libjpeg-dev \
    zlib1g-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . .

# Make startup scripts executable
RUN chmod +x start.sh start-simple.sh start-robust.sh start-django.sh

# Create necessary directories
RUN mkdir -p staticfiles
RUN mkdir -p /app/db
RUN mkdir -p /app/media

# Collect static files
RUN python manage.py collectstatic --no-input --clear

# Verify static files were collected
RUN echo "Static files collected:" && ls -la staticfiles/

# Run migrations
RUN python manage.py migrate

# Start command using Django-only startup script (most reliable)
CMD ["./start-django.sh"] 