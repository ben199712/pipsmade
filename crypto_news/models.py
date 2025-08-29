from django.db import models
from django.utils import timezone
import uuid

class CryptoNews(models.Model):
    """Model for storing crypto market news"""
    
    NEWS_CATEGORIES = [
        ('market', 'Market Analysis'),
        ('price', 'Price Action'),
        ('regulation', 'Regulation'),
        ('adoption', 'Adoption & Partnerships'),
        ('technology', 'Technology & Development'),
        ('defi', 'DeFi & NFTs'),
        ('trading', 'Trading & Volume'),
        ('general', 'General News'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    summary = models.TextField()
    content = models.TextField()
    source = models.CharField(max_length=100)
    source_url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=NEWS_CATEGORIES, default='general')
    
    # Crypto-specific fields
    related_coins = models.JSONField(default=list, help_text="List of related cryptocurrency symbols")
    sentiment = models.CharField(max_length=20, choices=[
        ('positive', 'Positive'),
        ('negative', 'Negative'),
        ('neutral', 'Neutral'),
    ], default='neutral')
    
    # Metadata
    published_at = models.DateTimeField()
    fetched_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    priority = models.IntegerField(default=1, help_text="Higher number = higher priority")
    
    # SEO and display
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    featured_image = models.URLField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Crypto News'
        verbose_name_plural = 'Crypto News'
        ordering = ['-published_at', '-priority']
        indexes = [
            models.Index(fields=['-published_at']),
            models.Index(fields=['category']),
            models.Index(fields=['sentiment']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            # Generate slug from title
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    @property
    def time_ago(self):
        """Return human-readable time since publication"""
        now = timezone.now()
        diff = now - self.published_at
        
        if diff.days > 0:
            return f"{diff.days} day{'s' if diff.days != 1 else ''} ago"
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        else:
            return "Just now"
    
    @property
    def short_summary(self):
        """Return truncated summary for display"""
        if len(self.summary) <= 100:
            return self.summary
        return self.summary[:97] + "..."
    
    def get_related_coins_display(self):
        """Return formatted related coins string"""
        if not self.related_coins:
            return "General"
        return ", ".join(self.related_coins[:3])  # Show max 3 coins
