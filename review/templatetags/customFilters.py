from django import template
from django.shortcuts import render
from django.template.defaultfilters import stringfilter
from django.template import loader
from django.template import Template
from datetime import datetime
 
register = template.Library()
 
### Filters ###
@register.filter
def subtract(value,args):
    if value=='':
        value=0
    if args=='':
        args=0
    return int(value)-int(args)
 
@register.filter
@stringfilter
def shrink(text, count):
    return text[:count]
 
 
# @register.filter(is_safe=True)
def nl2br(value):
    return value.replace('\\n', '<br />')