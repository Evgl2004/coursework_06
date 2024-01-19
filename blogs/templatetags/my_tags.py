from django import template

register = template.Library()


@register.filter()
def mediapath(input_value):
    if input_value:
        return f"/media/{input_value}"
    else:
        return '/media/НетФото.png'


@register.simple_tag
def mediapath_tag(input_value):
    if input_value:
        return f"/media/{input_value}"
    else:
        return '/media/НетФото.png'
