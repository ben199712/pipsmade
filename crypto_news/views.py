from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import CryptoNews

def get_latest_crypto_news(limit=3):
    """Get latest crypto news for display"""
    return CryptoNews.objects.filter(
        is_active=True
    ).order_by('-published_at', '-priority')[:limit]

class CryptoNewsListView(ListView):
    model = CryptoNews
    template_name = 'crypto_news/news_list.html'
    context_object_name = 'news_list'
    paginate_by = 10
    
    def get_queryset(self):
        return CryptoNews.objects.filter(
            is_active=True
        ).order_by('-published_at', '-priority')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = CryptoNews.NEWS_CATEGORIES
        context['page_title'] = 'Crypto Market News'
        return context

class CryptoNewsDetailView(DetailView):
    model = CryptoNews
    template_name = 'crypto_news/news_detail.html'
    context_object_name = 'news'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get related news from same category
        context['related_news'] = CryptoNews.objects.filter(
            category=self.object.category,
            is_active=True
        ).exclude(id=self.object.id).order_by('-published_at')[:3]
        return context
