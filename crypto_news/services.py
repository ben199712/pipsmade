import requests
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)

class CryptoNewsService:
    """Service for fetching crypto news"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'PipsMade-CryptoNews/1.0'
        })
    
    def fetch_news_from_cryptopanic(self, limit=10):
        """Fetch news from CryptoPanic API"""
        try:
            url = "https://cryptopanic.com/api/v1/posts/"
            params = {
                'filter': 'hot',
                'public': 'true',
                'limit': limit
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            news_items = []
            
            for item in data.get('results', []):
                try:
                    related_coins = []
                    if 'currencies' in item:
                        for currency in item['currencies']:
                            if 'code' in currency:
                                related_coins.append(currency['code'])
                    
                    sentiment = 'neutral'
                    if 'votes' in item:
                        votes = item['votes']
                        positive = votes.get('positive', 0)
                        negative = votes.get('negative', 0)
                        if positive > negative:
                            sentiment = 'positive'
                        elif negative > positive:
                            sentiment = 'negative'
                    
                    published_at = datetime.fromisoformat(
                        item['published_at'].replace('Z', '+00:00')
                    )
                    
                    news_items.append({
                        'title': item['title'],
                        'summary': item.get('metadata', {}).get('description', ''),
                        'source': item['source']['title'],
                        'source_url': item['url'],
                        'category': self._categorize_news(item['title']),
                        'related_coins': related_coins,
                        'sentiment': sentiment,
                        'published_at': published_at,
                        'priority': 1
                    })
                    
                except Exception as e:
                    logger.error(f"Error processing news item: {e}")
                    continue
            
            return news_items
            
        except Exception as e:
            logger.error(f"Error fetching news from CryptoPanic: {e}")
            return []
    
    def _categorize_news(self, title):
        """Categorize news based on title"""
        title_lower = title.lower()
        
        if any(word in title_lower for word in ['price', 'market', 'trading']):
            return 'trading'
        elif any(word in title_lower for word in ['regulation', 'sec', 'government']):
            return 'regulation'
        elif any(word in title_lower for word in ['adoption', 'partnership']):
            return 'adoption'
        elif any(word in title_lower for word in ['technology', 'upgrade']):
            return 'technology'
        else:
            return 'general'
