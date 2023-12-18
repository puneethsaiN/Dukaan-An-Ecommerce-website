from django import template
register = template.Library()

@register.simple_tag()
def subtract(qty, unit_price, *args, **kwargs):
    # you would need to do any localization of the result here
    return qty - unit_price