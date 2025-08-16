from django.shortcuts import render
from django.views.generic import TemplateView
from investments.models import InvestmentPlan
from django.db.models import Min, Max
import logging
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import os
import sqlite3
from pathlib import Path

logger = logging.getLogger(__name__)

class HomeView(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Home - Professional Investment Platform'
        
        try:
            # Get active investment plans for pricing section
            investment_plans = InvestmentPlan.objects.filter(is_active=True).order_by('min_investment')[:6]
            context['investment_plans'] = investment_plans
            
            # Calculate pricing statistics
            if investment_plans.exists():
                context['pricing_stats'] = {
                    'total_plans': investment_plans.count(),
                    'min_roi': investment_plans.aggregate(Min('min_roi_percentage'))['min_roi_percentage__min'] or 0,
                    'max_roi': investment_plans.aggregate(Max('max_roi_percentage'))['max_roi_percentage__max'] or 0,
                }
                logger.info(f"Loaded {context['pricing_stats']['total_plans']} investment plans for homepage")
            else:
                context['pricing_stats'] = {
                    'total_plans': 0,
                    'min_roi': 0,
                    'max_roi': 0,
                }
                logger.info("No active investment plans found for homepage")
                
        except Exception as e:
            logger.error(f"Error loading investment plans for homepage: {str(e)}")
            # Fallback values if there's an error
            context['investment_plans'] = []
            context['pricing_stats'] = {
                'total_plans': 0,
                'min_roi': 0,
                'max_roi': 0,
            }
        
        return context

class AboutView(TemplateView):
    template_name = 'about.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'About Us - pipsmade'
        return context

class ContactView(TemplateView):
    template_name = 'contact.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Contact Us - pipsmade'
        return context

def index(request):
    return render(request, 'index.html')

@csrf_exempt
@require_http_methods(["GET"])
def health_check(request):
    """Simple health check endpoint for monitoring"""
    try:
        # Check database connection
        db_path = Path(__file__).parent.parent / 'db.sqlite3'
        if db_path.exists():
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            conn.close()
            db_status = "healthy"
        else:
            db_status = "database file not found"
        
        # Check static files
        static_path = Path(__file__).parent.parent / 'staticfiles'
        if static_path.exists():
            static_status = "healthy"
            static_count = len(list(static_path.rglob('*')))
        else:
            static_status = "static files not found"
            static_count = 0
        
        return JsonResponse({
            'status': 'healthy',
            'timestamp': str(Path(__file__).parent.parent),
            'database': db_status,
            'static_files': static_status,
            'static_count': static_count,
            'environment': os.environ.get('DJANGO_SETTINGS_MODULE', 'not set'),
            'static_root': str(static_path),
            'static_url': '/static/'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'error': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def test_static(request):
    """Test endpoint to verify static file serving"""
    try:
        from django.conf import settings
        from django.contrib.staticfiles.finders import find
        
        # Try to find a static file
        test_file = find('test.txt')
        if test_file:
            with open(test_file, 'r') as f:
                content = f.read()
            return HttpResponse(f"Static file found: {test_file}<br>Content: {content}")
        else:
            return HttpResponse("Static file 'test.txt' not found. Static files may not be configured correctly.")
    except Exception as e:
        return HttpResponse(f"Error testing static files: {str(e)}")
