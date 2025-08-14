from django import forms
from decimal import Decimal
from .models import InvestmentPlan, UserInvestment

class InvestmentForm(forms.Form):
    """Form for creating new investments"""
    investment_plan = forms.ModelChoiceField(
        queryset=InvestmentPlan.objects.filter(is_active=True),
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'investmentPlan'
        }),
        empty_label="Select Investment Plan"
    )
    
    amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=Decimal('100.00'),
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter investment amount',
            'step': '0.01',
            'min': '100'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        plan = cleaned_data.get('investment_plan')
        amount = cleaned_data.get('amount')
        
        if plan and amount:
            # Validate minimum investment
            if amount < plan.min_investment:
                raise forms.ValidationError(
                    f'Minimum investment for {plan.name} is ${plan.min_investment}'
                )
            
            # Validate maximum investment
            if plan.max_investment and amount > plan.max_investment:
                raise forms.ValidationError(
                    f'Maximum investment for {plan.name} is ${plan.max_investment}'
                )
        
        return cleaned_data

class InvestmentCalculatorForm(forms.Form):
    """Form for investment calculator"""
    plan = forms.ModelChoiceField(
        queryset=InvestmentPlan.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=Decimal('100.00'),
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter amount to calculate returns'
        })
    )
