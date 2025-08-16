from django import forms
from django.contrib.auth.models import User
from .models import SupportTicket, SupportMessage, SupportCategory, SupportKnowledgeBase, SupportFAQ

class SupportTicketForm(forms.ModelForm):
    """Form for creating support tickets"""
    
    class Meta:
        model = SupportTicket
        fields = ['category', 'subject', 'priority', 'status', 'description']
        widgets = {
            'category': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Brief description of your issue',
                'required': True
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'status': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Provide detailed information about your issue...',
                'required': True
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].help_text = "Choose the category that best describes your issue"
        self.fields['subject'].help_text = "Brief description of your issue"
        self.fields['priority'].help_text = "How urgent is this issue?"
        self.fields['status'].help_text = "Current status of the issue"
        self.fields['description'].help_text = "Provide detailed information about your issue"

class SupportMessageForm(forms.ModelForm):
    """Form for adding messages to support tickets"""
    
    class Meta:
        model = SupportMessage
        fields = ['message', 'attachment']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Type your message here...',
                'required': True
            }),
            'attachment': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.jpg,.jpeg,.png,.pdf,.doc,.docx,.txt'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['message'].help_text = "Your message or response"
        self.fields['attachment'].help_text = "Optional: Upload screenshots, documents, or other relevant files (Max 10MB)"

class EmailSupportForm(forms.Form):
    """Form for email support requests"""
    
    TOPIC_CHOICES = [
        ('', 'Select a topic'),
        ('account', 'Account Issues'),
        ('deposit', 'Deposit Problems'),
        ('withdrawal', 'Withdrawal Issues'),
        ('investment', 'Investment Questions'),
        ('technical', 'Technical Support'),
        ('billing', 'Billing & Fees'),
        ('security', 'Security Concerns'),
        ('other', 'Other'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    topic = forms.ChoiceField(
        choices=TOPIC_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'required': True
        })
    )
    
    priority = forms.ChoiceField(
        choices=PRIORITY_CHOICES,
        initial='medium',
        widget=forms.Select(attrs={
            'class': 'form-select',
            'required': True
        })
    )
    
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Brief description of your issue',
            'required': True
        })
    )
    
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 6,
            'placeholder': 'Describe your issue in detail...',
            'required': True
        })
    )
    
    attachments = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.jpg,.jpeg,.png,.pdf,.doc,.docx,.txt'
        })
    )
    
    contact_email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your.email@example.com',
            'required': True
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['topic'].help_text = "Select the category that best describes your issue"
        self.fields['priority'].help_text = "How urgent is this issue?"
        self.fields['subject'].help_text = "Brief description of your issue"
        self.fields['message'].help_text = "Provide detailed information about your issue"
        self.fields['attachments'].help_text = "Optional: Upload screenshots, documents, or other relevant files (Max 5 files, 10MB each)"
        self.fields['contact_email'].help_text = "We'll use this email to contact you"

class QuickSupportForm(forms.Form):
    """Quick support form for common issues"""
    ISSUE_TYPES = [
        ('', 'Select an issue type'),
        ('login', 'Login Problems'),
        ('deposit', 'Deposit Issues'),
        ('withdrawal', 'Withdrawal Issues'),
        ('trading', 'Trading Problems'),
        ('account', 'Account Settings'),
        ('security', 'Security Concerns'),
        ('other', 'Other'),
    ]
    
    issue_type = forms.ChoiceField(
        choices=ISSUE_TYPES,
        widget=forms.Select(attrs={
            'class': 'form-select',
            'required': True
        })
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your.email@example.com',
            'required': True
        })
    )
    
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Describe your issue briefly...',
            'required': True
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['issue_type'].help_text = "Select the category that best describes your issue"
        self.fields['email'].help_text = "We'll use this email to contact you"
        self.fields['message'].help_text = "Provide a brief description of your issue"

class SupportSearchForm(forms.Form):
    """Form for searching support articles and FAQs"""
    
    query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search for help articles, FAQs...',
            'aria-label': 'Search support content'
        })
    )
    
    category = forms.ModelChoiceField(
        queryset=SupportCategory.objects.filter(is_active=True),
        required=False,
        empty_label="All Categories",
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

class AdminTicketUpdateForm(forms.ModelForm):
    """Form for admin staff to update tickets"""
    
    class Meta:
        model = SupportTicket
        fields = ['status', 'priority', 'assigned_to']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'assigned_to': forms.Select(attrs={'class': 'form-select'}),
        }
