from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
import re

register = template.Library()

@register.filter(name='addcss')
def addcss(field, css):
   return field.as_widget(attrs={"class": css})

@stringfilter
def spacify(value, autoescape=None):
   if autoescape:
      esc = conditional_escape
   else:
      esc = lambda x: x
   line_break = re.sub('\n', "<br>", esc(value))
   s = re.sub('\s', '&nbsp;', esc(line_break))
   return mark_safe(s)
spacify.needs_autoescape = False
register.filter(spacify)

@register.filter()
def field_type(field):
    return field.field.__class__.__name__

