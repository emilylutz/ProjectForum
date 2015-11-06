from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag
def navactive(request, string, urls):
    if request.path in (reverse(url) for url in urls.split()):
        return string
    return ''
