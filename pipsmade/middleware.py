"""
Custom middleware for debugging and CSRF handling
"""
import logging
from django.utils.deprecation import MiddlewareMixin
from django.middleware.csrf import CsrfViewMiddleware
from django.http import JsonResponse

logger = logging.getLogger(__name__)

class CSRFDebugMiddleware(MiddlewareMixin):
    """
    Middleware to debug CSRF issues and provide better error messages
    """
    
    def process_request(self, request):
        # Log request details for debugging
        logger.info(f"Request: {request.method} {request.path}")
        logger.info(f"Headers: {dict(request.headers)}")
        logger.info(f"CSRF Token in POST: {request.POST.get('csrfmiddlewaretoken', 'NOT_FOUND')}")
        logger.info(f"CSRF Token in Headers: {request.headers.get('X-CSRFToken', 'NOT_FOUND')}")
        
        return None
    
    def process_exception(self, request, exception):
        # Log CSRF exceptions specifically
        if isinstance(exception, Exception):
            logger.error(f"Exception in {request.path}: {str(exception)}")
            logger.error(f"Request method: {request.method}")
            logger.error(f"Request headers: {dict(request.headers)}")
        
        return None

class CSRFBypassMiddleware(MiddlewareMixin):
    """
    Temporary middleware to bypass CSRF for debugging
    WARNING: Only use for debugging, remove in production!
    """
    
    def process_request(self, request):
        # Skip CSRF for specific paths during debugging
        if request.path in ['/accounts/login/', '/accounts/signup/', '/csrf-test/']:
            logger.warning(f"CSRF bypassed for {request.path} - DEBUGGING ONLY!")
            # Set a flag to skip CSRF validation
            request._csrf_bypass = True
        
        return None
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        # Skip CSRF validation for bypassed paths
        if hasattr(request, '_csrf_bypass') and request._csrf_bypass:
            logger.warning(f"CSRF validation skipped for {request.path}")
            return None
        
        return None 