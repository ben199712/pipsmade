from django.contrib import admin
from .models import CryptoNews

@admin.register(CryptoNews)
class CryptoNewsAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'category', 'sentiment', 'source', 
        'related_coins_display', 'published_at', 'time_ago', 'is_active'
    ]
    list_filter = [
        'category', 'sentiment', 'source', 'is_active', 
        'published_at', 'fetched_at'
    ]
    search_fields = ['title', 'summary', 'content', 'source']
    readonly_fields = ['id', 'fetched_at', 'slug']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'summary', 'content', 'slug')
        }),
        ('Source & Category', {
            'fields': ('source', 'source_url', 'category', 'sentiment')
        }),
        ('Crypto Details', {
            'fields': ('related_coins', 'featured_image')
        }),
        ('Publication', {
            'fields': ('published_at', 'priority', 'is_active')
        }),
        ('Metadata', {
            'fields': ('id', 'fetched_at'),
            'classes': ('collapse',)
        }),
    )
    
    def related_coins_display(self, obj):
        if obj.related_coins:
            coins = obj.related_coins[:3]
            return ", ".join(coins)
        return "General"
    related_coins_display.short_description = "Related Coins"
    
    def time_ago(self, obj):
        return obj.time_ago
    time_ago.short_description = "Time Ago"
    
    list_per_page = 25
    date_hierarchy = 'published_at'
    ordering = ['-published_at', '-priority']
