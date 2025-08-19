from django.shortcuts import render
from .models import FAQCategory, FAQ

def faq_list(request):
    """Display all FAQ categories and questions"""
    categories = FAQCategory.objects.filter(is_active=True).prefetch_related('faqs')
    
    # Filter active FAQs for each category
    for category in categories:
        category.faqs = category.faqs.filter(is_active=True)
    
    context = {
        'categories': categories,
        'total_faqs': FAQ.objects.filter(is_active=True).count()
    }
    return render(request, 'faq/faq_list.html', context)

def faq_by_category(request, category_slug):
    """Display FAQs for a specific category"""
    try:
        category = FAQCategory.objects.get(slug=category_slug, is_active=True)
        faqs = category.faqs.filter(is_active=True)
    except FAQCategory.DoesNotExist:
        category = None
        faqs = []
    
    context = {
        'category': category,
        'faqs': faqs,
        'categories': FAQCategory.objects.filter(is_active=True)
    }
    return render(request, 'faq/faq_category.html', context)
