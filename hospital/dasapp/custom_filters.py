from django import template
from datetime import timedelta
from django.utils import timezone

register = template.Library()

@register.filter
def add_days(value, days):
    return value + timedelta(days=days)