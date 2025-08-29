from django.core.management.base import BaseCommand
from django.utils import timezone
from crypto_news.models import CryptoNews
from crypto_news.services import CryptoNewsService

class Command(BaseCommand):
    help = 'Fetch latest crypto news from APIs'

    def add_arguments(self, parser):
        parser.add_argument('--force', action='store_true', help='Force fetch')

    def handle(self, *args, **options):
        force = options['force']
        
        self.stdout.write('Starting crypto news fetch...')
        
        # Check if we have recent news (within 2 days)
        if not force:
            two_days_ago = timezone.now() - timezone.timedelta(days=2)
            recent_count = CryptoNews.objects.filter(
                fetched_at__gte=two_days_ago, is_active=True
            ).count()
            
            if recent_count >= 3:
                self.stdout.write(f'Found {recent_count} recent articles. Use --force to fetch.')
                return
        
        # Fetch news
        service = CryptoNewsService()
        news_items = service.fetch_news_from_cryptopanic(10)
        
        if news_items:
            self.stdout.write(f'Fetched {len(news_items)} articles')
            
            # Save news
            saved = 0
            for item in news_items:
                try:
                    CryptoNews.objects.create(
                        title=item['title'],
                        summary=item['summary'],
                        content=item['summary'],
                        source=item['source'],
                        source_url=item.get('source_url', ''),
                        category=item['category'],
                        related_coins=item['related_coins'],
                        sentiment=item['sentiment'],
                        published_at=item['published_at'],
                        priority=item['priority']
                    )
                    saved += 1
                except Exception as e:
                    self.stdout.write(f'Error saving: {e}')
                    continue
            
            self.stdout.write(f'Saved {saved} articles')
        else:
            self.stdout.write('No news fetched')
        
        # Clean old news
        week_ago = timezone.now() - timezone.timedelta(days=7)
        old_count = CryptoNews.objects.filter(fetched_at__lt=week_ago).count()
        CryptoNews.objects.filter(fetched_at__lt=week_ago).delete()
        
        if old_count > 0:
            self.stdout.write(f'Cleaned {old_count} old articles')
        
        total = CryptoNews.objects.filter(is_active=True).count()
        self.stdout.write(f'Total active articles: {total}')
