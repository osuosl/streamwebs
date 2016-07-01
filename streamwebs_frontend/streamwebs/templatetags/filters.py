from django.template import Library

register = Library()


@register.filter
def strtoul(value):
    """Converts spaces into underlines in a string"""
    return value.replace(' ', '_')
