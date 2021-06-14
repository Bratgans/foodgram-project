from django import template

register = template.Library()


@register.filter(name='get_filter_values')
def get_filter_values(value):
    return value.getlist('filters')


@register.filter(name='get_filter_link')
def get_filter_values(request, tag):
    """Изменение строки запроса в соответствии с выбранными тегами."""
    new_request = request.GET.copy()
    if tag.title in request.GET.getlist('filters'):
        filters = new_request.getlist('filters')
        filters.remove(tag.title)
        new_request.setlist('filters', filters)
    else:
        new_request.appendlist('filters', tag.title)
    return new_request.urlencode()
