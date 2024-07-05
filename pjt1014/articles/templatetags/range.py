from django import template

register = template.Library()


@register.filter()
def range_(count=10):
    return range(count)
