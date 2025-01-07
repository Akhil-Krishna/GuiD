from django import template

register = template.Library()

@register.filter
def dict_get(d, key):
    try:
        return d.get(key, None)
    except AttributeError:
        return None

@register.filter
def div(value, arg):
    """Divides the value by the argument"""
    try:
        return float(value) / float(arg)
    except (ValueError, ZeroDivisionError):
        return ''

@register.filter
def mul(value, arg):
    """Multiplies the value by the argument"""
    try:
        return float(value) * float(arg)
    except ValueError:
        return ''