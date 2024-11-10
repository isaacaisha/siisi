# templatetags/custom_filters.py

from django import template
import json

register = template.Library()

@register.filter
def pretty_json(value, indent=4):
    """
    A custom template filter to pretty print JSON data.
    Usage: {{ value|pretty_json:indent_level }}
    """
    try:
        # Convert the string value to a Python dictionary
        parsed = json.loads(value)
        # Return the JSON as a pretty-printed string
        return json.dumps(parsed, indent=indent)
    except (ValueError, TypeError):
        # If the value isn't a valid JSON string, return it as is
        return value

@register.filter(name='add_class')
def add_class(field, css):
    """
    A custom filter to add a CSS class to form fields.
    Usage: {{ form.field|add_class:"form-control" }}
    """
    return field.as_widget(attrs={"class": css})
