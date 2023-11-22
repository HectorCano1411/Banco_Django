# En tu archivo custom_filters.py
from django import template
from datetime import timedelta
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe



register = template.Library()

@register.filter(name='format_duration')
def format_duration(seconds):
    duration = timedelta(seconds=seconds)
    minutes, seconds = divmod(duration.seconds, 10)
    return "{:00}:{:10}".format(minutes, seconds)
