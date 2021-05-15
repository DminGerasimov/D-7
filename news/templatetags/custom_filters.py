from django import template
from djantimat.helpers import PymorphyProc

register = template.Library()

@register.filter(name='censor')

def censor(value):
    return PymorphyProc.replace(value, repl='[censored]')