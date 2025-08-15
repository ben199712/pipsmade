from django.shortcuts import render
from django.views.generic import TemplateView
from investments.models import InvestmentPlan
from django.db.models import Min, Max
import logging

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
