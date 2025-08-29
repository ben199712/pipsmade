from django import template
from crypto_news.models import CryptoNews

register = template.Library()

@register.simple_tag
def get_latest_crypto_news(limit=3):
    """Get latest crypto news for display"""
    return CryptoNews.objects.filter(
        is_active=True
    ).order_by('-published_at', '-priority')[:limit]

@register.simple_tag
def get_crypto_news_by_category(category, limit=3):
    """Get crypto news by category"""
    return CryptoNews.objects.filter(
        category=category,
        is_active=True
    ).order_by('-published_at', '-priority')[:limit]

@register.simple_tag
def get_crypto_news_count():
    """Get total count of active crypto news"""
    return CryptoNews.objects.filter(is_active=True).count()
