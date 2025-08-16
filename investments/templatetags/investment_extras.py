from django import template
from datetime import datetime, timedelta
from django.utils import timezone

register = template.Library()

@register.filter
def add_days(value, days):
    """Add days to a date"""
    try:
        return value + timedelta(days=int(days))
    except (ValueError, TypeError):
        return value

@register.filter
def add(value, arg):
    """Add arg to value"""
    try:
        return float(value) + float(arg)
    except (ValueError, TypeError):
        return value

@register.filter
def mul(value, arg):
    """Multiply value by arg"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return value

@register.filter
def asset_color(plan_type):
    """Get color for asset type"""
    colors = {
        'crypto': '#10B981',
        'stocks': '#3B82F6',
        'forex': '#F59E0B',
        'bonds': '#8B5CF6'
    }
    return colors.get(plan_type, '#6B7280')

@register.filter
def plan_icon(plan_type):
    """Get Font Awesome icon for plan type"""
    icons = {
        'crypto': 'fab fa-bitcoin',
        'stocks': 'fas fa-chart-line',
        'forex': 'fas fa-dollar-sign',
        'bonds': 'fas fa-university'
    }
    return icons.get(plan_type, 'fas fa-chart-pie') 