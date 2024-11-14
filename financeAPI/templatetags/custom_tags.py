from django import template
from django.utils import timezone

register = template.Library()


@register.filter
def multiply_by_two(value):
    try:
        return value ** 2
    except (TypeError, ValueError):
        return ""


@register.filter
def date(value):
    if value:
        value = timezone.datetime.fromisoformat(value)
    return value.strftime('%Y-%m-%d') if value else 'нет даты'