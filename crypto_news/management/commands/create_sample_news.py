from django.core.management.base import BaseCommand
from django.utils import timezone
from crypto_news.models import CryptoNews
from datetime import timedelta

class Command(BaseCommand):
    help = 'Create sample crypto news for testing'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample crypto news...')
        
        # Sample news data
        sample_news = [
            {
                'title': 'Bitcoin Surges Past $50,000 as Institutional Adoption Grows',
                'summary': 'Bitcoin has reached a new milestone, crossing the $50,000 mark for the first time in months. Major financial institutions continue to show interest in cryptocurrency investments.',
                'source': 'CryptoNews Daily',
                'category': 'price',
                'related_coins': ['BTC'],
                'sentiment': 'positive',
                'published_at': timezone.now() - timedelta(hours=2)
            },
            {
                'title': 'Ethereum 2.0 Upgrade Shows Promising Results',
                'summary': 'The latest Ethereum network upgrade has significantly improved transaction speeds and reduced gas fees, leading to increased developer activity on the platform.',
                'source': 'Blockchain Weekly',
                'category': 'technology',
                'related_coins': ['ETH'],
                'sentiment': 'positive',
                'published_at': timezone.now() - timedelta(hours=4)
            },
            {
                'title': 'SEC Approves New Crypto ETF Applications',
                'summary': 'The Securities and Exchange Commission has approved several new cryptocurrency ETF applications, signaling growing regulatory acceptance of digital assets.',
                'source': 'Financial Times',
                'category': 'regulation',
                'related_coins': ['BTC', 'ETH'],
                'sentiment': 'positive',
                'published_at': timezone.now() - timedelta(hours=6)
            },
            {
                'title': 'Major Bank Announces Crypto Custody Services',
                'summary': 'A leading global bank has announced plans to offer cryptocurrency custody services to institutional clients, marking a significant step in traditional finance adoption.',
                'source': 'Banking Today',
                'category': 'adoption',
                'related_coins': ['BTC', 'ETH', 'USDC'],
                'sentiment': 'positive',
                'published_at': timezone.now() - timedelta(hours=8)
            },
            {
                'title': 'DeFi Protocol Reports Record Trading Volume',
                'summary': 'Decentralized finance protocols have seen unprecedented trading volumes this month, with users increasingly turning to DeFi for yield farming opportunities.',
                'source': 'DeFi Pulse',
                'category': 'defi',
                'related_coins': ['UNI', 'AAVE', 'COMP'],
                'sentiment': 'positive',
                'published_at': timezone.now() - timedelta(hours=10)
            }
        ]
        
        created_count = 0
        for news_data in sample_news:
            try:
                CryptoNews.objects.create(
                    title=news_data['title'],
                    summary=news_data['summary'],
                    content=news_data['summary'],
                    source=news_data['source'],
                    category=news_data['category'],
                    related_coins=news_data['related_coins'],
                    sentiment=news_data['sentiment'],
                    published_at=news_data['published_at'],
                    priority=1,
                    is_active=True
                )
                created_count += 1
                self.stdout.write(f'Created: {news_data["title"]}')
            except Exception as e:
                self.stdout.write(f'Error creating news: {e}')
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} sample news articles!')
        )
        
        # Show total count
        total = CryptoNews.objects.filter(is_active=True).count()
        self.stdout.write(f'Total active news articles: {total}')
