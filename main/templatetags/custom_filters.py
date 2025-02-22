# In your app/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def dict_item(dictionary, key):
    return dictionary.get(str(key))