from django import forms
from .models import SupportTicket, SupportMessage, SupportCategory

class SupportTicketForm(forms.ModelForm):
    """Form for creating support tickets"""
    
    class Meta:
        model = SupportTicket
        fields = ['category', 'subject', 'description', 'priority']
        widgets = {
            'category': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Brief description of your issue',
                'maxlength': 200,
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Please provide detailed information about your issue...',
                'required': True
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show active categories
        self.fields['category'].queryset = SupportCategory.objects.filter(is_active=True)
        
        # Set help texts
        self.fields['subject'].help_text = "Enter a clear, concise subject line"
        self.fields['description'].help_text = "Provide as much detail as possible to help us resolve your issue quickly"
        self.fields['priority'].help_text = "Select the urgency level of your request"

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
                'accept': '.jpg,.jpeg,.png,.gif,.pdf,.doc,.docx,.txt'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['message'].help_text = "Add additional information or respond to support staff"
        self.fields['attachment'].help_text = "Optional: Upload screenshots, documents, or other relevant files (Max 10MB)"

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
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search for help articles, FAQs...',
            'autocomplete': 'off'
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
    """Form for admin to update ticket status and assignment"""
    
    class Meta:
        model = SupportTicket
        fields = ['status', 'priority', 'assigned_to']
        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select'
            }),
            'assigned_to': forms.Select(attrs={
                'class': 'form-select'
            })
        }
    
    admin_notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Internal notes (not visible to user)...'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show staff users for assignment
        from django.contrib.auth.models import User
        self.fields['assigned_to'].queryset = User.objects.filter(is_staff=True)
        self.fields['assigned_to'].empty_label = "Unassigned"
