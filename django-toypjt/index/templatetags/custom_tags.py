from django import template

register = template.Library()


@register.filter()
def slicer(value, arg: str):
    if len(arg) > 12:
        value = arg[:13] + "..."
    return value


@register.filter()
def color_changer(value, arg: int):
    color_list = (
        "",
        "text-danger fw-bolder",
        "text warning fw-bolder",
        "text-warning",
        "text-secondary",
        "text-white",
    )
    i = (25 - arg) // 5
    if arg > 20:
        value = "text-danger fw-bolder"
        return value
    else:
        value = color_list[i]
        return value


@register.filter()
def star_range(count=10):
    return range(count)
