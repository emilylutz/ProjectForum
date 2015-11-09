from django.http import Http404
from django.views.generic import TemplateView


class StyleGuideView(TemplateView):
    """ An admin only view that shows the Style Guide. """
    template_name = 'styleguide.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404("Page not found")
        return super(StyleGuideView, self).dispatch(request, *args, **kwargs)
