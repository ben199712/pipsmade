from django import template
from django.utils.safestring import mark_safe
from faq.models import FAQCategory, FAQ

register = template.Library()

@register.simple_tag
def get_faqs_by_category(category_name, limit=None):
    """Get FAQs for a specific category"""
    try:
        category = FAQCategory.objects.get(name=category_name, is_active=True)
        faqs = category.faqs.filter(is_active=True)
        if limit:
            faqs = faqs[:limit]
        return faqs
    except FAQCategory.DoesNotExist:
        return []

@register.simple_tag
def get_main_faqs(limit=6):
    """Get main platform FAQs for the home page"""
    try:
        category = FAQCategory.objects.get(name='Platform & Security', is_active=True)
        return category.faqs.filter(is_active=True)[:limit]
    except FAQCategory.DoesNotExist:
        return []

@register.simple_tag
def get_support_faqs(limit=3):
    """Get support FAQs for the contact page"""
    try:
        category = FAQCategory.objects.get(name='Support & Contact', is_active=True)
        return category.faqs.filter(is_active=True)[:limit]
    except FAQCategory.DoesNotExist:
        return []

@register.simple_tag
def render_faq_accordion(faqs, accordion_id='faqAccordion'):
    """Render FAQ accordion HTML"""
    if not faqs:
        return mark_safe('<p class="text-muted">No FAQs available at the moment.</p>')
    
    html = f'<div class="accordion" id="{accordion_id}">'
    
    for i, faq in enumerate(faqs, 1):
        is_first = i == 1
        collapse_class = 'collapse show' if is_first else 'collapse'
        button_class = 'accordion-button' if is_first else 'accordion-button collapsed'
        
        html += f'''
        <div class="accordion-item">
            <h2 class="accordion-header" id="faq{i}">
                <button class="{button_class}" type="button" data-bs-toggle="collapse" data-bs-target="#collapse{i}">
                    {faq.question}
                </button>
            </h2>
            <div id="collapse{i}" class="accordion-collapse {collapse_class}" data-bs-parent="#{accordion_id}">
                <div class="accordion-body">
                    {faq.answer}
                </div>
            </div>
        </div>
        '''
    
    html += '</div>'
    return mark_safe(html) 