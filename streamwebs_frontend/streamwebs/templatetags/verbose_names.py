from django import template
register = template.Library()


@register.simple_tag
def get_field_label(instance, field_name):
    """
    Returns verbose_name for a field.
    """
    return instance[field_name].label
