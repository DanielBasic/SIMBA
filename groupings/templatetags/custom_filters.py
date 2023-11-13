from django import template
from django.utils.safestring import mark_safe
from django.template import Library
import json

register = Library()

@register.filter
def get_key(dictionary, key):
    return dictionary.get(key, None)

@register.filter(is_safe=True)
def js(obj):
    return mark_safe(json.dumps(obj))