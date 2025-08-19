from django.core.management.base import BaseCommand
from faq.models import FAQCategory, FAQ

class Command(BaseCommand):
    help = 'Populate FAQ database with existing content'

    def handle(self, *args, **options):
        self.stdout.write('Creating FAQ categories and questions...')
        
        # Create Platform FAQ category
        platform_category, created = FAQCategory.objects.get_or_create(
            name='Platform & Security',
            defaults={
                'description': 'Questions about platform security, investments, and general platform usage',
                'order': 1
            }
        )
        if created:
            self.stdout.write(f'✅ Created category: {platform_category.name}')
        else:
            self.stdout.write(f'📝 Category already exists: {platform_category.name}')
        
        # Create Support FAQ category
        support_category, created = FAQCategory.objects.get_or_create(
            name='Support & Contact',
            defaults={
                'description': 'Questions about customer support, consultations, and contact information',
                'order': 2
            }
        )
        if created:
            self.stdout.write(f'✅ Created category: {support_category.name}')
        else:
            self.stdout.write(f'📝 Category already exists: {support_category.name}')
        
        # Platform FAQ questions (from index.html)
        platform_faqs = [
            {
                'question': 'How secure are my investments?',
                'answer': 'Your investments are protected by bank-level security measures, including SSL encryption, two-factor authentication, and segregated client accounts. We\'re fully regulated and insured up to $500,000 per account.',
                'order': 1,
                'is_featured': True
            },
            {
                'question': 'What is the minimum investment amount?',
                'answer': 'Our minimum investment starts at $500 for the Starter plan. This allows new investors to begin their journey with a manageable amount while still accessing professional trading strategies.',
                'order': 2
            },
            {
                'question': 'How often can I withdraw my funds?',
                'answer': 'You can request withdrawals at any time. Processing typically takes 1-3 business days for bank transfers and 24 hours for cryptocurrency withdrawals. There are no withdrawal fees for amounts over $100.',
                'order': 3
            },
            {
                'question': 'What markets do you trade in?',
                'answer': 'We trade across multiple markets including cryptocurrencies (Bitcoin, Ethereum, etc.), stocks (S&P 500, NASDAQ), bonds (government and corporate), and forex pairs (EUR/USD, GBP/USD, etc.).',
                'order': 4
            },
            {
                'question': 'Are the returns guaranteed?',
                'answer': 'Investment returns are not guaranteed and past performance doesn\'t predict future results. However, our experienced team and proven strategies have consistently delivered strong returns within the expected ranges for each risk level.',
                'order': 5
            },
            {
                'question': 'How do I track my investment performance?',
                'answer': 'You\'ll have access to a comprehensive dashboard showing real-time portfolio performance, detailed reports, and transaction history. We also provide regular email updates and mobile app notifications.',
                'order': 6
            }
        ]
        
        # Support FAQ questions (from contact.html)
        support_faqs = [
            {
                'question': 'How quickly will I receive a response?',
                'answer': 'We typically respond to all inquiries within 2-4 hours during business hours. For urgent matters, please use our live chat or call our support line.',
                'order': 1,
                'is_featured': True
            },
            {
                'question': 'Can I schedule a consultation?',
                'answer': 'Yes! We offer free 30-minute consultations with our investment advisors. You can schedule one through our booking system or by calling our support team.',
                'order': 2
            },
            {
                'question': 'What information should I prepare?',
                'answer': 'For investment consultations, please have your financial goals, risk tolerance, and current portfolio information ready. For technical support, account details and error descriptions are helpful.',
                'order': 3
            }
        ]
        
        # Create Platform FAQs
        for faq_data in platform_faqs:
            faq, created = FAQ.objects.get_or_create(
                question=faq_data['question'],
                category=platform_category,
                defaults={
                    'answer': faq_data['answer'],
                    'order': faq_data['order'],
                    'is_featured': faq_data.get('is_featured', False)
                }
            )
            if created:
                self.stdout.write(f'✅ Created FAQ: {faq.question[:50]}...')
            else:
                self.stdout.write(f'📝 FAQ already exists: {faq.question[:50]}...')
        
        # Create Support FAQs
        for faq_data in support_faqs:
            faq, created = FAQ.objects.get_or_create(
                question=faq_data['question'],
                category=support_category,
                defaults={
                    'answer': faq_data['answer'],
                    'order': faq_data['order'],
                    'is_featured': faq_data.get('is_featured', False)
                }
            )
            if created:
                self.stdout.write(f'✅ Created FAQ: {faq.question[:50]}...')
            else:
                self.stdout.write(f'📝 FAQ already exists: {faq.question[:50]}...')
        
        self.stdout.write(self.style.SUCCESS('🎉 FAQ population completed successfully!'))
        self.stdout.write(f'📊 Total Categories: {FAQCategory.objects.count()}')
        self.stdout.write(f'📊 Total FAQs: {FAQ.objects.count()}') 