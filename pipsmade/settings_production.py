"""
Production settings for Railway deployment
"""
from .settings import *

# Production settings
DEBUG = False
ALLOWED_HOSTS = ['.railway.app', '.up.railway.app', '*']

# Database - Use SQLite for Railway
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static files
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'

# Security settings
SECURE_SSL_REDIRECT = False  # Railway handles SSL
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

# Email backend for production
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' 