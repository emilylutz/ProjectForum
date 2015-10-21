from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from .forms import RegisterForm
from .models import RegistrationLink

class ActivateView(TemplateView):
    """
    User activation view.
    """
    template_name = 'register_activate.html'
    success_url = 'profile:activate_complete'

    def get(self, request, *args, **kwargs):
        if RegistrationLink.objects.activate_by_key(*args, **kwargs):
            return redirect(self.success_url)
        return super(ActivateView, self).get(request, *args, **kwargs)

class RegisterView(FormView):
    """
    User registration views.
    """
    template_name = 'register_form.html'
    form_class = RegisterForm
    success_url = 'profile:register_complete'

    def form_valid(self, form):
        site = get_current_site(self.request)
        model = get_user_model()

        data = form.cleaned_data
        new_user = model.objects.create_user(
            username=data.get('username'),
            email=data.get('email'),
            password=data.get('password1'),
        )
        registration_link = RegistrationLink.objects.create_inactive_user(
            site, new_user, self.request)

        return redirect(self.success_url)
