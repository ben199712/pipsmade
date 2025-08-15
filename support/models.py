from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class SupportCategory(models.Model):
    """Support ticket categories"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default='fas fa-question-circle')
    color = models.CharField(max_length=20, default='primary')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Support Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

class SupportTicket(models.Model):
    """Support tickets from users"""
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('waiting_user', 'Waiting for User'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]

    # Basic Information
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='support_tickets')
    category = models.ForeignKey(SupportCategory, on_delete=models.SET_NULL, null=True)
    subject = models.CharField(max_length=200)
    description = models.TextField()

    # Status and Priority
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')

    # Assignment
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tickets',
        limit_choices_to={'is_staff': True}
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    # Additional Info
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"#{self.id} - {self.subject}"

    def get_status_color(self):
        colors = {
            'open': 'danger',
            'in_progress': 'warning',
            'waiting_user': 'info',
            'resolved': 'success',
            'closed': 'secondary',
        }
        return colors.get(self.status, 'primary')

    def get_priority_color(self):
        colors = {
            'low': 'success',
            'medium': 'warning',
            'high': 'danger',
            'urgent': 'dark',
        }
        return colors.get(self.priority, 'primary')

    def mark_resolved(self):
        """Mark ticket as resolved"""
        self.status = 'resolved'
        self.resolved_at = timezone.now()
        self.save()

    def mark_closed(self):
        """Mark ticket as closed"""
        self.status = 'closed'
        self.closed_at = timezone.now()
        self.save()

class SupportMessage(models.Model):
    """Messages within support tickets"""
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_staff_reply = models.BooleanField(default=False)

    # Attachments
    attachment = models.FileField(upload_to='support_attachments/', null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Message in ticket #{self.ticket.id}"

class SupportKnowledgeBase(models.Model):
    """Knowledge base articles"""
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.ForeignKey(SupportCategory, on_delete=models.CASCADE)

    # SEO and Search
    slug = models.SlugField(unique=True)
    keywords = models.CharField(max_length=500, blank=True)

    # Status
    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    # Stats
    view_count = models.PositiveIntegerField(default=0)
    helpful_votes = models.PositiveIntegerField(default=0)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']

    def __str__(self):
        return self.title

class SupportFAQ(models.Model):
    """Frequently Asked Questions"""
    question = models.CharField(max_length=300)
    answer = models.TextField()
    category = models.ForeignKey(SupportCategory, on_delete=models.CASCADE)

    # Display
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    # Stats
    view_count = models.PositiveIntegerField(default=0)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'question']
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question
