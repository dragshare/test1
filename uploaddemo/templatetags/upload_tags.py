import os

from django.utils.safestring import mark_safe

from django import template

register = template.Library()

@register.filter
def basename(path):
    output = ''
    if path:
        output = os.path.basename(path)
    return mark_safe(output)
