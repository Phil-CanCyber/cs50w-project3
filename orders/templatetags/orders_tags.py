from django import template
import locale
locale.setlocale(locale.LC_ALL, '')

register = template.Library()

# used like dictionary|hash:key
# credit to https://push.cx/2007/django-template-tag-for-dictionary-access
@register.filter
def hash(h, key):
    try:
        return h[key]
    except:
        return None

@register.filter
def dict_length(h):
    return len(h)

# credit to: https://djangosnippets.org/snippets/552/
@register.filter()
def currency(value):
    return locale.currency(value, grouping=True)