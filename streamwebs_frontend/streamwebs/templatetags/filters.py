from django.template import Library
from django.utils.translation import ugettext_lazy as _

register = Library()


@register.filter
def strtoul(value):
    """Converts spaces into underlines in a string"""
    return value.replace(' ', '_')


@register.filter
def slashtoul(value):
    """Converts slash into underline in a string"""
    return value.replace('/', '_')


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
        return _("Set 15' rope at 20' from the water")
    elif index == 1:
        return _("At 40' from the water")
    elif index == 2:
        return _("At 60' from the water")
    elif index == 3:
        return _("At 80' from the water")
    elif index == 4:
        return _("At 100' from the water")


@register.filter
def get_zone_labels(category):
    """Grabs translatable zone-table header string"""
    if category == 'zone':
        return _('Zone')
    elif category == 'conifers':
        return _('Conifers')
    elif category == 'hardwoods':
        return _('Hardwoods')
    elif category == 'shrubs':
        return _('Shrubs')
    elif category == 'comments':
        return _('Comments')


@register.filter
def get_cc_percentage(est_cc):
    """Calculates a percentage for the estimated canopy cover"""
    percentage = ((float(est_cc) / 96) * 100)
    return ("{0:.2f}".format(percentage))
