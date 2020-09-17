from django import template

register = template.Library()


@register.filter(name='times')
def times(number):
    """
    Args:
        number:
    """
    return range(number)
