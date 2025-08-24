"""
Production settings for Railway deployment
"""
from .settings import *
import os

# Production settings
DEBUG = False
ALLOWED_HOSTS = ['.railway.app', '.up.railway.app', 'pipsmade.com', 'www.pipsmade.com',]

# Database - Use SQLite for Railway
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static files configuration
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Additional static files directories
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Static files finders
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# CSRF Configuration - Fix for 403 errors
CSRF_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_TRUSTED_ORIGINS = [
    'https://pipsmade.com',
    'https://www.pipsmade.com',
    'https://*.railway.app',
    'https://*.up.railway.app',
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'https://localhost:8000',
    'https://127.0.0.1:8000',
]

# Additional CSRF settings for debugging
CSRF_FAILURE_VIEW = 'django.views.csrf.csrf_failure'
CSRF_USE_SESSIONS = False
CSRF_COOKIE_NAME = 'csrftoken'

# Session Configuration
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# Security settings
SECURE_SSL_REDIRECT = False  # Railway handles SSL
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Add custom middleware for CSRF debugging
MIDDLEWARE.insert(0, 'pipsmade.middleware.CSRFDebugMiddleware')
MIDDLEWARE.insert(1, 'pipsmade.middleware.CSRFBypassMiddleware')

# Logging - Enhanced for CSRF debugging
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
    'loggers': {
        'django.security.csrf': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'pipsmade.middleware': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

# Email backend for production
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# WhiteNoise for static files (if available)
try:
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
except:
    pass 