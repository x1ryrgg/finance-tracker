from django import template

register = template.Library()


@register.filter
def multiply_by_two(value):
    try:
        return value ** 2
    except (TypeError, ValueError):
        return ""  # Возврат пустой строки, если есть ошибка