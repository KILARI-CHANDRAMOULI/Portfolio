import json

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name="to_json")
def to_json(value):
    """Render a Python list/dict as a JSON string safe for an HTML attribute."""
    return mark_safe(json.dumps(value).replace("'", "&#39;"))


@register.filter(name="initials")
def initials(value):
    """'Chandra Mouli Kilari' -> 'CK' (first and last word initials)."""
    parts = [p for p in str(value or "").split() if p]
    if not parts:
        return "?"
    if len(parts) == 1:
        return parts[0][:2].upper()
    return (parts[0][0] + parts[-1][0]).upper()


@register.filter(name="split")
def split(value, sep=","):
    return [item.strip() for item in str(value or "").split(sep) if item.strip()]
