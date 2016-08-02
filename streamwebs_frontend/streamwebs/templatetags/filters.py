from django.template import Library

register = Library()


@register.filter
def strtoul(value):
    """Converts spaces into underlines in a string"""
    return value.replace(' ', '_')


@register.filter
def namespace(value):
    """Converts URL references to namespaced references"""
    return "streamwebs:" + value


@register.filter
def plus_one(index):
    """
    Takes a list index and adds one so that it looks like a list starts from
    1, not 0
    """
    return index + 1


@register.filter
def get_zone(index):
    """Grabs a zone description based on form order"""
    if index == 0:
        return "Set 15' rope at 20' from the water"
    elif index == 1:
        return "At 40' from the water"
    elif index == 2:
        return "At 60' from the water"
    elif index == 3:
        return "At 80' from the water"
    elif index == 4:
        return "At 100' from the water"
