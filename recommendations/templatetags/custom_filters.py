from django import template

register = template.Library()


@register.filter
def replace(value, old, new):
    """Replace occurrences of *old* with *new* in the given string.

    Usage in template:
      {{ value|replace:"_"," " }}
    """
    try:
        return value.replace(old, new)
    except Exception:
        return value
