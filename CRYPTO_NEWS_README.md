# 📰 Crypto News System

## Overview
The crypto news system automatically fetches and displays live cryptocurrency market news on your index page, replacing the old Trading Signals section.

## Features
- ✅ **Live News Updates**: Fetches news from CryptoPanic API every 2 days
- ✅ **Smart Categorization**: Automatically categorizes news by type
- ✅ **Sentiment Analysis**: Shows positive/negative market sentiment
- ✅ **Related Coins**: Identifies which cryptocurrencies are mentioned
- ✅ **Admin Interface**: Easy management through Django admin
- ✅ **Responsive Design**: Works on all devices

## How It Works

### 1. **News Sources**
- **CryptoPanic API**: Primary source for crypto news
- **Automatic Updates**: Fetches news every 2 days
- **Smart Filtering**: Only shows relevant, high-quality news

### 2. **News Display**
- **Index Page**: Shows 3 latest news articles in the right sidebar
- **News List Page**: Full list of all news articles (`/crypto-news/`)
- **News Detail Page**: Individual article view with full content

### 3. **News Categories**
- Market Analysis
- Price Action
- Regulation
- Adoption & Partnerships
- Technology & Development
- DeFi & NFTs
- Trading & Volume
- General News

## Setup Instructions

### 1. **Install Dependencies**
```bash
pip install requests
```

### 2. **Run Migrations**
```bash
python manage.py makemigrations crypto_news
python manage.py migrate
```

### 3. **Fetch Initial News**
```bash
python manage.py fetch_crypto_news
```

### 4. **Test the System**
- Visit your homepage to see live crypto news
- Check `/crypto-news/` for the full news list
- Use Django admin to manage news articles

## Management Commands

### Fetch Latest News
```bash
python manage.py fetch_crypto_news
```

### Force Fetch (Ignore 2-day limit)
```bash
python manage.py fetch_crypto_news --force
```

### Schedule News Fetch
```bash
python manage.py schedule_news_fetch
```

## Admin Interface

### Access
- Go to `/admin/` and log in
- Look for "Crypto News Management" section

### Features
- View all news articles
- Edit news content and metadata
- Control which news are active
- Set priority levels
- Monitor sentiment and categories

## Automation

### Manual Setup (Recommended for now)
Run this command every 2 days:
```bash
python manage.py fetch_crypto_news
```

### Future Automation Options
- **Cron Jobs**: Set up server cron jobs
- **Celery**: Use Django Celery for background tasks
- **Railway Cron**: Use Railway's built-in cron functionality

## Customization

### Change News Display Count
In `templates/index.html`, modify:
```html
{% get_latest_crypto_news 3 as latest_news %}
```
Change `3` to any number you want.

### Modify News Sources
Edit `crypto_news/services.py` to add more news APIs.

### Custom Categories
Modify `NEWS_CATEGORIES` in `crypto_news/models.py`.

## Troubleshooting

### No News Displaying
1. Check if news were fetched: `python manage.py fetch_crypto_news`
2. Verify news are marked as active in admin
3. Check Django logs for errors

### API Errors
1. Verify internet connection
2. Check if CryptoPanic API is accessible
3. Review error logs in Django admin

### Template Errors
1. Ensure `crypto_news_tags` is loaded in templates
2. Check template syntax
3. Verify URL patterns are correct

## API Limits

### CryptoPanic
- **Free Tier**: 100 requests per hour
- **Rate Limiting**: Automatic throttling
- **Data Freshness**: Updates every few minutes

## Security Notes

### Data Sources
- All news come from trusted crypto news APIs
- Content is filtered for relevance
- No user-generated content

### Admin Access
- Only staff users can manage news
- News content is read-only for regular users
- Sentiment analysis is automated

## Performance

### Caching
- News are cached in database
- Updates every 2 days to minimize API calls
- Efficient database queries with proper indexing

### Scalability
- System can handle thousands of news articles
- Automatic cleanup of old news (7+ days)
- Optimized for production use

---

## Quick Start Checklist

- [ ] Run migrations
- [ ] Fetch initial news
- [ ] Check admin interface
- [ ] Test homepage display
- [ ] Set up automation (optional)

Your crypto news system is now ready! 🎉
